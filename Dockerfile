FROM python:3.9
WORKDIR /work

# install basic dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    apt-transport-https ca-certificates gnupg curl sudo \
    && rm -rf /var/lib/apt/lists/*

# install basic packages
COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY ./ /work

CMD exec uvicorn --port $PORT --host 0.0.0.0 app.main:app
