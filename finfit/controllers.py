from flask import current_app
from .airtable_api import FinFit
from APIException import APIException
import os
import json

def get_org_data(rid):
    if rid:
        # Access the configuration settings
        arg = {'app': current_app.config['APP_FINFIT'], "table": current_app.config['TABLE_AGENTS']}
        api_key = current_app.config['AIRTABLE_API_KEY']
        finfit = FinFit(api_key, arg)
        data = finfit.get_dynamic_data(rid)
        return data
    else:
    	raise APIException('Invalid request - Query parameter rid is missing', status_code=400)