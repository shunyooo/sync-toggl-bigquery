_VERSION:=1.0.0
_IMAGE:=toggl-bigquery
_SERVICE:=${_IMAGE}-test
_API_PROJECT_NAME:=ToggleBigQuery
_REGION:=asia-northeast1
_GCP_BQ_DATASET_ID:=toggl
_TOGGL_TIMEZONE:=jst
_TOGGL_API_TOKEN:=****
_GCP_PROJECT_ID:=****
_SERVICE_ACCOUNT:=toggle-timer@****.iam.gserviceaccount.com

.PHONY: up
up:
	docker-compose up --build

.PHONY: deploy
deploy:	
	gcloud builds submit \
	--substitutions ^:^_PROJECT=${_GCP_PROJECT_ID}\
	:_VERSION=${_VERSION}\
	:_API_ENV="GCP_BQ_DATASET_ID=${_GCP_BQ_DATASET_ID},\
	          TOGGL_TIMEZONE=${_TOGGL_TIMEZONE},\
              TOGGL_API_TOKEN=${_TOGGL_API_TOKEN},\
              API_VERSION=${_VERSION},\
              API_PROJECT_NAME=${_API_PROJECT_NAME},\
              GCP_PROJECT_ID=${_GCP_PROJECT_ID},\
              GCP_LOCATION=${_REGION}"\
	:_SERVICE=${_SERVICE}\
	:_IMAGE=${_IMAGE}\
	:_REGION=${_REGION}\
	:_SERVICE_ACCOUNT=${_SERVICE_ACCOUNT}\
	 --project ${_GCP_PROJECT_ID}
