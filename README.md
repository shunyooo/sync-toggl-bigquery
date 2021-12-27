# toggle track to BigQuery

Sync logs of toggl track to BigQuery continuously



## Quick Start

### Step-1: Create BigQuery Dataset

Create a dataset, like **`toggl`** for example.



### Step-2: Create Service Account and Add Roles

Create a service account as `toggle-timer@{project_id}.iam.gserviceaccount.com` and grant it the permissions of BigQuery Admin.

![Group 1](https://user-images.githubusercontent.com/17490886/115999718-ca209380-a627-11eb-8fce-1edfc1fa2a2d.png)

The account for the build should also be given the roles as follows.

![Group 2](https://user-images.githubusercontent.com/17490886/115999847-6e0a3f00-a628-11eb-861b-2793f9eb8862.png)



### Step-3: Setting

```
_VERSION:=1.0.0
_IMAGE:=toggl-bigquery
_SERVICE:=${_IMAGE}
_API_PROJECT_NAME:=ToggleBigQuery
_REGION:=asia-northeast1
_GCP_BQ_DATASET_ID:=toggl
_TOGGL_TIMEZONE:=jst
_TOGGL_API_TOKEN:=*****
_GCP_PROJECT_ID:=*****
_SERVICE_ACCOUNT:=toggle-timer@*****.iam.gserviceaccount.com
```



### Step-3: Build & Deploy Cloud Run App

```
make deploy/prd
```



### Step-4: Create Trigger

```
gcloud beta scheduler jobs create http export_recent_entries_toggl_to_bigquery \
   --schedule '0 * * * *' \
   --uri ${CLOUD_RUN_URL} \
   --http-method 'get' \
   --attempt-deadline '30m' \
   --description 'Export Toggl to BigQuery' \
   --time-zone 'Asia/Tokyo'
```

