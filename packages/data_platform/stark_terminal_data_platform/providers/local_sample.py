from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import (
    DataProviderType,
    DataQualityStatus,
    MarketDataRequestKind,
    ProviderCapability,
    ProviderStatus,
    Timeframe,
)
from stark_terminal_core.domain.identifiers import DataProviderId
from stark_terminal_core.domain.market_data import MarketDataBar
from stark_terminal_core.domain.market_data_contracts import MarketDataRequest, MarketDataResponse
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import (
    SyntheticOHLCVConfig,
    generate_synthetic_ohlcv_bars,
)
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.instruments.master import LocalInstrumentMaster
from stark_terminal_data_platform.providers.approval import (
    approve_for_design,
    create_provider_approval_record,
)
from stark_terminal_data_platform.providers.base import MarketDataProvider
from stark_terminal_data_platform.providers.contracts import ProviderCapabilityReport
from stark_terminal_data_platform.providers.guardrails import (
    ProviderGuardrailDecision,
    ProviderGuardrailPolicy,
    ProviderGuardrailResult,
    ProviderIntegrationMode,
    default_provider_guardrail_policy,
    evaluate_provider_guardrails,
)
from stark_terminal_data_platform.providers.readiness import ProviderComplianceChecklist
from stark_terminal_data_platform.quality.builtins import MarketDataResponseValidator
from stark_terminal_data_platform.quality.enums import ValidationStatus


LOCAL_SAMPLE_SOURCE_REFERENCE = "synthetic-local-test-only"
LOCAL_SAMPLE_PROVIDER_ID = DataProviderId(
    name="local_sample",
    provider_type=DataProviderType.LOCAL_SAMPLE,
    version="v0",
)
SUPPORTED_LOCAL_SAMPLE_CAPABILITIES = [
    ProviderCapability.INSTRUMENT_MASTER,
    ProviderCapability.HISTORICAL_BARS,
    ProviderCapability.HEALTH_CHECK,
]
UNSUPPORTED_LOCAL_SAMPLE_CAPABILITIES = [
    ProviderCapability.LATEST_BAR,
    ProviderCapability.OPTIONS_CHAIN,
    ProviderCapability.FUTURES_CHAIN,
    ProviderCapability.CORPORATE_ACTIONS,
]


class LocalSampleProviderHealthStatus(BaseModel):
    enabled: bool
    provider_name: str
    provider_type: str
    synthetic_only: bool = True
    real_data_allowed: bool = False
    network_allowed: bool = False
    credentials_required: bool = False
    capabilities: list[str]
    guardrail_decision: str
    status: str
    error: str | None = None


def _synthetic_approval_record(capabilities: Iterable[ProviderCapability]):
    record = create_provider_approval_record(
        provider_name=LOCAL_SAMPLE_PROVIDER_ID.name,
        requested_capabilities=list(capabilities),
        requester="stark_terminal_prompt_21",
        requested_mode=ProviderIntegrationMode.SYNTHETIC_ONLY,
        notes=[
            "Local Sample Provider Adapter v0 uses synthetic local fixtures only.",
            "No network calls, scraping, credentials, real ingestion, or execution behavior.",
        ],
    )
    return approve_for_design(record, reviewer="stark_terminal_guardrails")


def _synthetic_compliance_checklist() -> ProviderComplianceChecklist:
    return ProviderComplianceChecklist(
        provider_name=LOCAL_SAMPLE_PROVIDER_ID.name,
        terms_review_completed=True,
        redistribution_allowed=False,
        storage_allowed=False,
        scraping_prohibited=True,
        credential_handling_reviewed=False,
        rate_limits_documented=False,
        data_quality_plan_ready=True,
        audit_logging_plan_ready=True,
        notes=[
            "Synthetic local sample provider; no real provider terms, credentials, or network calls.",
        ],
    )


def _timeframe_delta(timeframe: Timeframe) -> timedelta:
    if timeframe == Timeframe.DAILY:
        return timedelta(days=1)
    if timeframe == Timeframe.FIFTEEN_MINUTE:
        return timedelta(minutes=15)
    if timeframe == Timeframe.FIVE_MINUTE:
        return timedelta(minutes=5)
    raise ValueError("local sample provider supports DAILY, FIFTEEN_MINUTE, and FIVE_MINUTE")


def _bars_for_requested_range(request: MarketDataRequest, settings: Settings) -> int:
    if request.start is None or request.end is None or request.timeframe is None:
        return settings.local_sample_provider_default_bar_count
    step = _timeframe_delta(request.timeframe)
    span = request.end - request.start
    if span <= timedelta(0):
        return 0
    possible = int(span / step) + 1
    return max(1, min(settings.local_sample_provider_default_bar_count, possible))


class LocalSampleProviderAdapter(MarketDataProvider):
    provider_id = LOCAL_SAMPLE_PROVIDER_ID

    def __init__(
        self,
        settings: Settings | None = None,
        instrument_master: LocalInstrumentMaster | None = None,
        guardrail_policy: ProviderGuardrailPolicy | None = None,
        approval=None,
        compliance: ProviderComplianceChecklist | None = None,
    ) -> None:
        resolved_settings = settings or get_settings()
        super().__init__(network_calls_allowed=False)
        self.settings = resolved_settings
        self.instrument_master = instrument_master or LocalInstrumentMaster(
            create_sample_instruments(),
            source="synthetic-local-test-only",
            schema_version=resolved_settings.market_data_contract_schema_version,
        )
        self.guardrail_policy = guardrail_policy or default_provider_guardrail_policy(resolved_settings)
        self.approval = approval or _synthetic_approval_record(SUPPORTED_LOCAL_SAMPLE_CAPABILITIES)
        self.compliance = compliance or _synthetic_compliance_checklist()
        self.response_validator = MarketDataResponseValidator(settings=resolved_settings)

    def evaluate_guardrails(self) -> ProviderGuardrailResult:
        return evaluate_provider_guardrails(
            provider_name=self.provider_id.name,
            requested_capabilities=SUPPORTED_LOCAL_SAMPLE_CAPABILITIES,
            policy=self.guardrail_policy,
            approval=self.approval,
            compliance=self.compliance,
        )

    def capabilities(self) -> ProviderCapabilityReport:
        guardrail_result = self.evaluate_guardrails()
        enabled = (
            self.settings.local_sample_provider_enabled
            and guardrail_result.decision == ProviderGuardrailDecision.ALLOW
            and not self.settings.local_sample_provider_allow_network
            and not self.settings.local_sample_provider_allow_real_data
        )
        return ProviderCapabilityReport(
            provider=self.provider_id,
            status=ProviderStatus.ENABLED if enabled else ProviderStatus.DISABLED,
            capabilities=SUPPORTED_LOCAL_SAMPLE_CAPABILITIES if enabled else [ProviderCapability.HEALTH_CHECK],
            network_calls_allowed=False,
            schema_version=self.settings.local_sample_provider_schema_version,
            notes=[
                "Local Sample Provider Adapter v0.",
                "Synthetic local sample test/dev only; no external provider, no live data, no credentials.",
                f"Guardrail decision: {guardrail_result.decision.value}.",
            ],
        )

    def health_check(self) -> LocalSampleProviderHealthStatus:
        try:
            guardrail_result = self.evaluate_guardrails()
            enabled = self.settings.local_sample_provider_enabled
            healthy = enabled and guardrail_result.decision == ProviderGuardrailDecision.ALLOW
            return LocalSampleProviderHealthStatus(
                enabled=enabled,
                provider_name=self.provider_id.name,
                provider_type=self.provider_id.provider_type.value,
                synthetic_only=True,
                real_data_allowed=False,
                network_allowed=False,
                credentials_required=False,
                capabilities=[capability.value for capability in SUPPORTED_LOCAL_SAMPLE_CAPABILITIES],
                guardrail_decision=guardrail_result.decision.value,
                status="HEALTHY" if healthy else "BLOCKED",
                error=None if healthy else "; ".join(guardrail_result.reasons),
            )
        except Exception as exc:  # pragma: no cover - defensive safety path
            return LocalSampleProviderHealthStatus(
                enabled=False,
                provider_name=self.provider_id.name,
                provider_type=self.provider_id.provider_type.value,
                synthetic_only=True,
                real_data_allowed=False,
                network_allowed=False,
                credentials_required=False,
                capabilities=[capability.value for capability in SUPPORTED_LOCAL_SAMPLE_CAPABILITIES],
                guardrail_decision=ProviderGuardrailDecision.BLOCK.value,
                status="UNHEALTHY",
                error=str(exc).replace("://", "://[redacted]"),
            )

    def _guardrails_allow(self) -> tuple[bool, str | None]:
        if not self.settings.local_sample_provider_enabled:
            return False, "Local sample provider is disabled"
        if self.settings.local_sample_provider_allow_network:
            return False, "Local sample provider network calls are forbidden"
        if self.settings.local_sample_provider_allow_real_data:
            return False, "Local sample provider real data is forbidden"
        result = self.evaluate_guardrails()
        if result.decision != ProviderGuardrailDecision.ALLOW:
            return False, "; ".join(result.reasons)
        return True, None

    def _safe_error_response(self, request: MarketDataRequest, reason: str) -> MarketDataResponse:
        return MarketDataResponse(
            request_id=request.request_id,
            kind=request.kind,
            provider=self.provider_id,
            quality_status=DataQualityStatus.REJECTED,
            source_data_reference=LOCAL_SAMPLE_SOURCE_REFERENCE,
            errors=[reason],
        )

    def _validate_response(self, response: MarketDataResponse) -> MarketDataResponse:
        report = self.response_validator.validate(response)
        if report.status in {ValidationStatus.FAIL, ValidationStatus.BLOCKED}:
            return MarketDataResponse(
                request_id=response.request_id,
                kind=response.kind,
                provider=self.provider_id,
                quality_status=DataQualityStatus.REJECTED,
                source_data_reference=LOCAL_SAMPLE_SOURCE_REFERENCE,
                errors=["Local sample provider response failed data quality validation"],
            )
        return response

    def get_instrument_master(self, request: MarketDataRequest) -> MarketDataResponse:
        allowed, reason = self._guardrails_allow()
        if not allowed:
            return self._safe_error_response(request, reason or "Local sample provider guardrails blocked request")
        if request.kind not in {
            MarketDataRequestKind.INSTRUMENT_MASTER,
            MarketDataRequestKind.HEALTH_CHECK,
        }:
            return self._safe_error_response(
                request,
                "Local sample provider instrument master supports only instrument master and health check requests",
            )
        response = MarketDataResponse(
            request_id=request.request_id,
            kind=request.kind,
            provider=self.provider_id,
            instruments=self.instrument_master.list_instruments(),
            quality_status=DataQualityStatus.NORMALIZED,
            source_data_reference=LOCAL_SAMPLE_SOURCE_REFERENCE,
        )
        return self._validate_response(response)

    def get_historical_bars(self, request: MarketDataRequest) -> MarketDataResponse:
        allowed, reason = self._guardrails_allow()
        if not allowed:
            return self._safe_error_response(request, reason or "Local sample provider guardrails blocked request")
        if request.kind != MarketDataRequestKind.HISTORICAL_BARS:
            return self._safe_error_response(
                request,
                "Local sample provider historical bars require HISTORICAL_BARS request kind",
            )
        missing = [
            name
            for name in ("instrument_id", "timeframe", "start", "end")
            if getattr(request, name) is None
        ]
        if missing:
            return self._safe_error_response(
                request,
                f"Local sample historical bars request missing required fields: {', '.join(missing)}",
            )
        if request.timeframe not in {Timeframe.DAILY, Timeframe.FIFTEEN_MINUTE, Timeframe.FIVE_MINUTE}:
            return self._safe_error_response(
                request,
                "Local sample provider supports only DAILY, FIFTEEN_MINUTE, and FIVE_MINUTE historical bars",
            )

        bar_count = _bars_for_requested_range(request, self.settings)
        if bar_count <= 0:
            return self._safe_error_response(request, "Local sample historical bars request range is empty")

        config = SyntheticOHLCVConfig(
            instrument_id=request.instrument_id,
            timeframe=request.timeframe,
            start_timestamp=request.start,
            bar_count=bar_count,
            start_price=self.settings.local_sample_provider_default_start_price,
            seed=self.settings.local_sample_provider_default_seed,
            provider=self.provider_id,
            quality_status=DataQualityStatus.RAW,
            source_data_reference=LOCAL_SAMPLE_SOURCE_REFERENCE,
        )
        bars = generate_synthetic_ohlcv_bars(config)
        if request.end is not None:
            bars = [bar for bar in bars if bar.timestamp <= request.end]
        return self._validated_bar_response(request, bars)

    def _validated_bar_response(
        self,
        request: MarketDataRequest,
        bars: list[MarketDataBar],
    ) -> MarketDataResponse:
        if not bars:
            return self._safe_error_response(request, "Local sample provider generated no synthetic bars")
        response = MarketDataResponse(
            request_id=request.request_id,
            kind=request.kind,
            provider=self.provider_id,
            bars=bars,
            quality_status=DataQualityStatus.RAW,
            source_data_reference=LOCAL_SAMPLE_SOURCE_REFERENCE,
        )
        return self._validate_response(response)

    def get_latest_bar(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._safe_error_response(
            request,
            "Local sample provider does not support real latest bars; use synthetic historical bars only",
        )

    def get_options_chain(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._safe_error_response(
            request,
            "Local sample provider does not support options chains; no real provider data is available",
        )

    def get_futures_chain(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._safe_error_response(
            request,
            "Local sample provider does not support futures chains; no real provider data is available",
        )


def create_local_sample_provider(settings: Settings | None = None) -> LocalSampleProviderAdapter:
    return LocalSampleProviderAdapter(settings=settings)


def sample_historical_bars_request(settings: Settings | None = None) -> MarketDataRequest:
    resolved_settings = settings or get_settings()
    instrument = create_sample_instruments()[0]
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end = start + timedelta(days=min(5, resolved_settings.local_sample_provider_default_bar_count))
    return MarketDataRequest(
        kind=MarketDataRequestKind.HISTORICAL_BARS,
        instrument_id=instrument.instrument_id,
        timeframe=Timeframe.DAILY,
        start=start,
        end=end,
        provider=LOCAL_SAMPLE_PROVIDER_ID,
        schema_version=resolved_settings.local_sample_provider_schema_version,
    )
