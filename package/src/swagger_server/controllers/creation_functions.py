from .general_functions import _add_timestamp
from .global_vars import MDBC


def _create(asset, metadata):
    metadata = _timestamp_metadata(metadata)
    _id = MDBC.insert_one({'asset': asset, 'metadata': metadata}).inserted_id
    return str(_id)

def _component_weighting_equal_one(metadata):
    components = metadata.get('components')
    sum_of_weights = 0
    for item in components:
        sum_of_weights += item.get('weighting')
    if sum_of_weights == 1:
        return True
    else:
        return False

def _timestamp_metadata(metadata):
    if not metadata.get('timestamp'):
        return _add_timestamp(metadata)
    else:
        return metadata
