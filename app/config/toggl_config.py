import os
from toggl import api, utils

config = utils.Config.factory(None)
config.api_token = os.environ["TOGGL_API_TOKEN"]
config.timezone = os.environ["TOGGL_TIMEZONE"]
