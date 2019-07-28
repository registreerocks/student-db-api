import datetime

from .global_vars import MDBC

def _add_timestamp(dictionary):
    dictionary['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    return dictionary

def _get_many_assets(param_dict):
    results = list(MDBC.find(param_dict))
    for r in results:
        r['_id'] = str(r['_id'])
    return results

def _get_one_asset(param_dict):
    result = MDBC.find_one(param_dict)
    result['_id'] = str(result['_id'])
    return result