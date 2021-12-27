from time import time
from typing import List

from app.config.gcp_config import GCP_PROJECT_ID
from app.functions.bigquey import (add_created_at_now, entry_table,
                                   project_table)
from app.functions.toggl import iter_all_project, iter_recent_time_entries
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator

router = APIRouter()


class ExportResult(BaseModel):
    is_success: bool
    messages: List[str]
    elapsed_sec: float


@router.get("/export_recent_entries_toggl_to_bigquery", response_model=ExportResult)
async def export_recent_entries_toggl_to_bigquery():
    print("export_recent_entries_toggl_to_bigquery")
    st_time = time()
    entries = list(iter_recent_time_entries())
    add_created_at_now(entries)
    print(entries)
    res = entry_table.add_rows(entries)
    elapsed_sec = time() - st_time
    if len(res) > 0:
        return ExportResult(is_success=False, messages=res, elapsed_sec=elapsed_sec)
    return ExportResult(is_success=True, messages=["success"], elapsed_sec=elapsed_sec)


@router.get("/export_all_projects_toggl_to_bigquery", response_model=ExportResult)
async def export_all_projects_toggl_to_bigquery():
    print("export_all_projects_toggl_to_bigquery")
    st_time = time()
    projects = list(iter_all_project())
    add_created_at_now(projects)
    print(projects)
    res = project_table.add_rows(projects)
    elapsed_sec = time() - st_time
    if len(res) > 0:
        return ExportResult(is_success=False, messages=res, elapsed_sec=elapsed_sec)
    return ExportResult(is_success=True, messages=["success"], elapsed_sec=elapsed_sec)
