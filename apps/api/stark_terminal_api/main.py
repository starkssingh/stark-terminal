from fastapi import FastAPI

from stark_terminal_api.routes.cache import router as cache_router
from stark_terminal_api.routes.config import router as config_router
from stark_terminal_api.routes.data_quality import router as data_quality_router
from stark_terminal_api.routes.database import router as database_router
from stark_terminal_api.routes.event_backbone import router as event_backbone_router
from stark_terminal_api.routes.features import router as features_router
from stark_terminal_api.routes.fixtures import router as fixtures_router
from stark_terminal_api.routes.health import router as health_router
from stark_terminal_api.routes.instrument_metadata import router as instrument_metadata_router
from stark_terminal_api.routes.instruments import router as instruments_router
from stark_terminal_api.routes.local_file_provider import router as local_file_provider_router
from stark_terminal_api.routes.local_sample_provider import router as local_sample_provider_router
from stark_terminal_api.routes.market_data_batches import router as market_data_batches_router
from stark_terminal_api.routes.provider_guardrails import router as provider_guardrails_router
from stark_terminal_api.routes.provider_readiness import router as provider_readiness_router
from stark_terminal_api.routes.research_lake import router as research_lake_router
from stark_terminal_api.routes.streams import router as streams_router
from stark_terminal_api.routes.synthetic_ohlcv_storage import router as synthetic_ohlcv_storage_router
from stark_terminal_api.routes.synthetic_ohlcv_exports import router as synthetic_ohlcv_exports_router
from stark_terminal_api.routes.timeseries import router as timeseries_router
from stark_terminal_api.routes.warehouse import router as warehouse_router
from stark_terminal_api.routes.workers import router as workers_router

app = FastAPI(
    title="Stark Terminal API",
    version="0.1.0",
    description="Prompt 25 institutional-grade foundation API shell.",
)

app.include_router(health_router)
app.include_router(config_router)
app.include_router(database_router)
app.include_router(timeseries_router)
app.include_router(research_lake_router)
app.include_router(cache_router)
app.include_router(streams_router)
app.include_router(event_backbone_router)
app.include_router(data_quality_router)
app.include_router(instrument_metadata_router)
app.include_router(market_data_batches_router)
app.include_router(synthetic_ohlcv_storage_router)
app.include_router(synthetic_ohlcv_exports_router)
app.include_router(provider_guardrails_router)
app.include_router(provider_readiness_router)
app.include_router(local_sample_provider_router)
app.include_router(local_file_provider_router)
app.include_router(workers_router)
app.include_router(instruments_router)
app.include_router(warehouse_router)
app.include_router(features_router)
app.include_router(fixtures_router)
