from app.api.routes import toggl_bigquery
from fastapi import APIRouter

router = APIRouter()

router.include_router(toggl_bigquery.router, tags=["toggl_bigquery"])
