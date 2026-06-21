from fastapi import FastAPI

from stark_terminal_api.routes.cache import router as cache_router
from stark_terminal_api.routes.config import router as config_router
from stark_terminal_api.routes.data_quality import router as data_quality_router
from stark_terminal_api.routes.database import router as database_router
from stark_terminal_api.routes.event_backbone import router as event_backbone_router
from stark_terminal_api.routes.features import router as features_router
from stark_terminal_api.routes.health import router as health_router
from stark_terminal_api.routes.instruments import router as instruments_router
from stark_terminal_api.routes.research_lake import router as research_lake_router
from stark_terminal_api.routes.streams import router as streams_router
from stark_terminal_api.routes.timeseries import router as timeseries_router
from stark_terminal_api.routes.warehouse import router as warehouse_router
from stark_terminal_api.routes.workers import router as workers_router

app = FastAPI(
    title="Stark Terminal API",
    version="0.1.0",
    description="Prompt 13 institutional-grade foundation API shell.",
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
app.include_router(workers_router)
app.include_router(instruments_router)
app.include_router(warehouse_router)
app.include_router(features_router)
