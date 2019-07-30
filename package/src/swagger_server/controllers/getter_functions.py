from bson.objectid import ObjectId

from .general_functions import _get_many_assets, _get_one_asset
from .global_vars import MDBC

def _get_asset_by_id(asset_id, meta_flag):
    asset = _get_one_asset({'_id': ObjectId(asset_id)})
    if not meta_flag:
        return {'data': asset.get('asset').get('data'), 'id': asset.get('_id')}
    else:
        return {'data': asset.get('asset').get('data'), 'id': asset.get('_id'), 'metadata': asset.get('metadata')}

def _get_assets(query_dict, meta_flag):
    files = _get_many_assets(query_dict)
    if not meta_flag:
        assets = [{k: v for k, v in f.items() if k != 'metadata'} for f in files]
        return assets
    else:
        return files

def _get_assets_by_type(asset_type, meta_flag):
    return _get_assets({'asset.data.asset_type': asset_type}, meta_flag)
   
def _get_assets_by_key(asset, key, value, meta_flag):
    return _get_assets({'asset.data.asset_type': asset, 'asset.data.'+key: value}, meta_flag)

def _get_children(_id, meta_flag, parent_name, child_name):
    return _get_assets({'asset.data.asset_type': child_name, 'asset.data.'+parent_name+'_id': _id}, meta_flag)

def _get_marks_by_student(student_address):
    mark_assets = get_student_mark_assets(student_address)
    degree_ids, course_ids, mark_data = process(mark_assets)
    mark_data = add_course_info(mark_data, course_ids)
    mark_data = add_degree_info(mark_data, degree_ids)
    return mark_data

def get_student_mark_assets(student_address):
    return list(_get_many_assets({'asset.data.asset_type':'mark', 'asset.data.student_address': student_address}))

def process(mark_assets):
    course_ids = list()
    degree_ids = list()
    marks = dict()
    for m in mark_assets:
        mark_data = m['asset']['data']
        mark_metadata = m['metadata']
        course_id = m['asset']['data']['course_id']
        degree_id = m['asset']['data']['degree_id']
        
        if not marks.get(course_id):
            marks[course_id] = dict()
            marks[course_id]['components'] = {mark_data['type']: {'mark': mark_metadata['mark'], 'timestamp': mark_metadata['timestamp'], 'degree_id': mark_data['degree_id']}}
        else:
            marks[course_id]['components'][mark_data['type']] = {'mark': mark_metadata['mark'], 'timestamp': mark_metadata['timestamp'], 'degree_id': mark_data['degree_id']}
            
        course_ids.append(course_id)
        degree_ids.append(degree_id)
        
    course_ids = list(set(course_ids))
    degree_ids = list(set(degree_ids))
    
    return (degree_ids, course_ids, marks)

def add_course_info(marks, course_ids):
    for course_id in course_ids:
        course = _get_one_asset({'_id': ObjectId(course_id)})
        
        if marks.get(course_id).get('year', '1900') < course['metadata']['timestamp'][:4]:
            marks.get(course_id)['year'] = course['metadata']['timestamp'][:4]
        
        marks[course_id] = {**marks[course_id], **course['asset']['data']}
        for c in course['metadata']['components']:
            if marks[course_id]['components'].get(c['type']):
                marks[course_id]['components'][c['type']]['weighting'] = c['weighting']
            
    return marks

def add_degree_info(marks, degree_ids):
    degree_data = dict()
    for degree_id in degree_ids:
        degree_data[degree_id] = _get_one_asset({'_id': ObjectId(degree_id)})
    return {'degree_data': degree_data, 'mark_data': marks}

# def _get_course_marks_by_lecturer(lecturer):
#     courses = _get_assets_by_key('course', 'lecturer', lecturer, True)
#     course_ids = [item.get('id') for item in courses]
#     marks_per_course = dict()
#     student_addresses = set()
#     for i, course_id in enumerate(course_ids):
#         marks = _get_assets_by_key('mark', 'course_id', course_id, True)
#         course_marks = dict()
#         for mark in marks:
#             student_address = mark.get('data').get('student_address')
#             mark_data = {'id': mark.get('id'), 'type': mark.get('data').get('type'), 'mark': mark.get('metadata').get('mark')}
#             if not course_marks.get(student_address):
#                 course_marks[student_address] = [mark_data]
#             else:
#                 course_marks[student_address].append(mark_data)
#             student_addresses.add(student_address)
#         marks_per_course[course_id] = {'name': courses[i].get('data').get('name'), 'components': courses[i].get('metadata').get('components'), 'course_marks': course_marks}
#     return {'student_addresses': list(student_addresses), 'marks_per_course': marks_per_course}
