import mock
import pytest
import pymongo
from bson.objectid import ObjectId


from src.swagger_server.controllers.getter_functions import (_get_assets,  # _retrieve_course_ids,; _retrieve_course_information,; _retrieve_degree_data,; _retrieve_mark_data
                                                             _get_asset_by_id,
                                                             _get_assets_by_key,
                                                             _get_marks_by_student)


@mock.patch('pymongo.collection.Collection.find')
def test_get_assets(mock_mongo_find):
    mock_mongo_find.return_value = get_course_blob()
    asset_type = "course"
    assert(_get_assets(asset_type, False) == get_course_assets())
    assert(_get_assets(asset_type, True) == get_course_blob())

@mock.patch('pymongo.collection.Collection.find')
def test_get_assets_by_key(mock_mongo_find):
    mock_mongo_find.return_value = get_course_blob()
    asset_type = "course"
    key = 'id'
    value = 'Econ104'
    assert(_get_assets_by_key(asset_type, key, value, False) == get_course_assets())
    assert(_get_assets_by_key(asset_type, key, value, True) == get_course_blob())

@mock.patch('pymongo.collection.Collection.find_one')
def test_get_asset_by_id(mock_mongo_find_one):
    mock_mongo_find_one.return_value = get_course_blob()[0]
    asset_id = ObjectId("5d7a4090b61d9af587ffa1b4")
    assert(_get_asset_by_id(asset_id, False) == get_course_by_id_result_only_asset()[0])
    assert(_get_asset_by_id(asset_id, True) == get_course_by_id_result()[0])

@mock.patch('pymongo.collection.Collection.find')
@mock.patch('pymongo.collection.Collection.find_one')
def test_get_marks_by_student(mock_mongo_find_one, mock_mongo_find):
    mock_mongo_find.return_value = get_mark_blob()
    mock_mongo_find_one.side_effect = [get_course_blob()[0], get_degree_blob()[0]]

    expected_output = {
        'degree_data': {'5d7a4090b61d9af587ffa1b4': get_degree_blob()[0]},
        'mark_data':{
            '5d7a4090b61d9af587ffa1b4': {
                'asset_type': 'course',
                'name': 'Econometrics',
                'description': 'This course is an introductory course in Econometrics',
                'id': 'Econ104',
                'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023",
                'year': '2018',
                'lecturer': 'Smith',
                'components': {
                    'midterm': {
                        'mark': 85,
                        'weighting': 0.25, 
                        'degree_id': '5d7a4090b61d9af587ffa1b4',
                        'timestamp': '2018-09-10 16:00'
                    }
                }
            }
        }
    }

    assert(_get_marks_by_student('0x03') == expected_output)


# @mock.patch('bigchaindb_driver.BigchainDB.transactions')
# @mock.patch('bigchaindb_driver.BigchainDB.assets')
# def test_get_course_marks_by_lecturer(mock_assets, mock_transactions):
#     mock_assets.get.side_effect = [get_course_assets(), get_mark_blob()]
#     mock_transactions.get.side_effect = [get_course_by_id_result(), get_mark_search_result()]
#     expected_output = {'student_addresses': ['0x03'], 
#     'marks_per_course':
#         {'6f4a3c43ec664373720ce1f8158b2779cfa0aec85954791a8ca766a1e53ef8bb': {
#             'name': 'Econometrics',
#             'components': [{
#                 'type': 'midterm', 
#                 'weighting': 0.25, 
#                 'required': True},
#                 {'type': 'final', 
#                 'weighting': 0.75, 
#                 'required': True}], 
#             'course_marks': {
#                 '0x03': [{
#                     '_id': '893e409d441b7f93bbad361053d43d9d9d82e570b5ff39c7fc43d83c96e509b0',
#                     'type': 'midterm',
#                     'mark': 85
#             }]}}}}
#     assert(_get_course_marks_by_lecturer('Smith')==expected_output)



def get_course_blob():
    return [{
            'metadata': {
                'timestamp': '2018-09-10 16:00',
                'passing': 60,
                'distinction': 90,
                'components': [{
                    'type': 'midterm', 
                    'weighting': 0.25, 
                    'required': True},
                    {'type': 'final', 
                    'weighting': 0.75, 
                    'required': True}],
                'prerequisite': [],
                'corequisite': []                },
            'asset': {
                'data': {
                    'asset_type': 'course',
                    'name': 'Econometrics',
                    'description': 'This course is an introductory course in Econometrics',
                    'id': 'Econ104',
                    'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023",
                    'lecturer': 'Smith'}},
            '_id': '5d7a4090b61d9af587ffa1b4'}]

def get_course_assets():
    return [{
            'asset': {
                'data': {
                    'asset_type': 'course',
                    'name': 'Econometrics',
                    'description': 'This course is an introductory course in Econometrics',
                    'id': 'Econ104',
                    'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023",
                    'lecturer': 'Smith'}
            },
            '_id': '5d7a4090b61d9af587ffa1b4'
        }]

def get_course_by_id_result():
    return [{
            'metadata': {
                'timestamp': '2018-09-10 16:00',
                'passing': 60,
                'distinction': 90,
                'components': [{
                    'type': 'midterm', 
                    'weighting': 0.25, 
                    'required': True},
                    {'type': 'final', 
                    'weighting': 0.75, 
                    'required': True}],
                'prerequisite': [],
                'corequisite': [],
            },
            'data': {
                'asset_type': 'course',
                'name': 'Econometrics',
                'description': 'This course is an introductory course in Econometrics',
                'id': 'Econ104',
                'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023",
                'lecturer': 'Smith'},
            '_id': '5d7a4090b61d9af587ffa1b4'}]

def get_course_by_id_result_only_asset():
    return [{
            'data': {
                'asset_type': 'course',
                'name': 'Econometrics',
                'description': 'This course is an introductory course in Econometrics',
                'id': 'Econ104',
                'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023",
                'lecturer': 'Smith'},
            '_id': '5d7a4090b61d9af587ffa1b4'}]

def get_mark_blob():
    return [{
        'asset': {
            'data': {
                'asset_type': 'mark',
                'student_address': '0x03',
                'course_id': '5d7a4090b61d9af587ffa1b4',
                'degree_id': '5d7a4090b61d9af587ffa1b4',
                'type': 'midterm'},
            },
        'metadata': {
            'mark': 85, 
            'timestamp': '2018-09-10 16:00'
        },
        '_id': '5d7a4090b61d9af587ffa1b4'}]

def get_degree_blob():
    return [{
            'metadata': {
                'courses': [{
                    'course_id': '5d7a4090b61d9af587ffa1b4', 
                    'weighting': 1, 
                    'semester': 1
                    }]
                },
            'asset': {
                'data': {
                    'asset_type': 'degree',
                    'level': 'Master',
                    'name': 'Fintech',
                    'description': 'This course is cool degree',
                    'id': 'MPhil-Fintech',
                    'university_id': "ece3537ac407a502e0586fbb8ad76771479cfd0689a38013b91ee77d97452023"}},
            '_id': '5d7a4090b61d9af587ffa1b4'}]