import time
from datetime import datetime, timedelta, timezone

from app.config.toggl_config import config
from pydantic import BaseModel
from toggl import api, utils


def iter_all_project():
    # Iterate All Project
    for p in api.Project.objects.all(config=config):
        proj_dict = p.to_dict()
        proj_dict["workspace_id"] = p.workspace.id
        proj_dict["client_id"] = p.client.id
        del proj_dict["client"], proj_dict["workspace"]
        time.sleep(1)
        yield proj_dict


def get_attribute(obj, attr_name, post_process):
    if obj is None:
        return None
    attr = obj.__getattribute__(attr_name)
    return post_process(attr)


def process_if_not_none(obj, process):
    return process(obj) if obj is not None else None


def _to_timestamp(dt):
    return dt.timestamp()


def _get_id(obj):
    return obj.id


def iter_time_entries(st_time, end_time):
    # Iterate Time Entries
    iter_reports = api.TimeEntry.objects.all_from_reports(
        config=config, start=st_time, stop=end_time
    )
    for report in iter_reports:
        time.sleep(1)
        report_dict = report.to_dict()
        report_dict["project_id"] = process_if_not_none(report.project, _get_id)
        report_dict["workspace_id"] = process_if_not_none(report.workspace, _get_id)
        report_dict["start"] = process_if_not_none(report.start, _to_timestamp)
        report_dict["stop"] = process_if_not_none(report.stop, _to_timestamp)
        del report_dict["project"], report_dict["tags"], report_dict["workspace"]
        yield report_dict


def iter_recent_time_entries():
    JST = timezone(timedelta(hours=+9), "JST")
    st_time = datetime.now(JST) - timedelta(days=1)
    end_time = st_time + timedelta(days=1)
    return iter_time_entries(st_time, end_time)
