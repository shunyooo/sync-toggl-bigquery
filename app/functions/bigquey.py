import time

from app.config.gcp_config import GCP_BQ_DATASET_ID, GCP_PROJECT_ID
from google.cloud import bigquery

client = bigquery.Client()


def add_created_at_now(_dict_list):
    now = time.time()
    for d in _dict_list:
        d["created_at"] = now


class BigQueryTable(object):
    def __init__(self, table_name, schema=None):
        self.table_id = f"{GCP_PROJECT_ID}.{GCP_BQ_DATASET_ID}.{table_name}"
        self.schema = schema

    def is_exists(self):
        try:
            client.get_table(self.table_id)
            return True
        except:
            return False

    def delete(self):
        if self.is_exists():
            client.delete_table(self.table_id)
        else:
            print(f"{self.table_id} is not exists")

    def create(self):
        assert self.schema is not None, "schema not defined"
        table = bigquery.Table(self.table_id, schema=self.schema)
        return client.create_table(table)

    def add_rows(self, rows):
        res = client.insert_rows_json(self.table_id, rows)
        if len(res) > 0:
            print("insert failed")
        return res


project_table = BigQueryTable(
    "project",
    [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("active", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("is_private", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("billable", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("auto_estimates", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("estimated_hours", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("color", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("hex_color", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("rate", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("workspace_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("client_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
    ],
)

entry_table = BigQueryTable(
    "time_entry",
    [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("task", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("billable", "BOOLEAN", mode="NULLABLE"),
        bigquery.SchemaField("start", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("stop", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("duration", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("created_with", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("project_id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("workspace_id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
    ],
)
