import mock
import pytest
import pymongo
from bson.objectid import ObjectId
import random

from src.swagger_server.controllers.querying_functions import _get_top_x, _get_top_x_percent, _query_bulk

@mock.patch('pymongo.collection.Collection.find')
def test_get_top_x(mock_mongo_find):
  mock_mongo_find.return_value = get_course_average_blob()
  assert(len(_get_top_x(10, 'course', '5d7a4090b61d9af587ffa1b4')) == 10)
  assert(len(_get_top_x(20, 'course', '5d7a4090b61d9af587ffa1b4')) == 20)
  assert(len(_get_top_x(25, 'course', '5d7a4090b61d9af587ffa1b4')) == 20)
  output = _get_top_x(10, 'course', '5d7a4090b61d9af587ffa1b4')
  student_addresses = [item['student_address'] for item in output]
  assert(len(list(set(student_addresses))) == 10)


@mock.patch('pymongo.collection.Collection.find')
def test_get_top_x_percent(mock_mongo_find):
  mock_mongo_find.return_value = get_course_average_blob()
  assert(len(_get_top_x_percent(10, 'course', '5d7a4090b61d9af587ffa1b4')) == 2)
  assert(len(_get_top_x_percent(50, 'course', '5d7a4090b61d9af587ffa1b4')) == 10)
  assert(len(_get_top_x_percent(100, 'course', '5d7a4090b61d9af587ffa1b4')) == 20)
  output = _get_top_x_percent(50, 'course', '5d7a4090b61d9af587ffa1b4')
  student_addresses = [item['student_address'] for item in output]
  assert(len(list(set(student_addresses))) == 10)

@mock.patch('pymongo.collection.Collection.find')
def test_bulk_query(mock_mongo_find):
  mock_mongo_find.return_value = get_course_average_blob()
  query_list = [{
    'type': 'course',
    'type_id': '5d7a4090b61d9af587ffa1b4',
    'x': 2,
    'absolute': True
    },
    {
    'type': 'course',
    'type_id': '5d7a4090b61d9af587ffa1b4',
    'x': 50,
    'absolute': False
    }]
  result =_query_bulk(query_list)
  assert(len(result) == 2)
  assert(len(result[0]) == 2)
  assert(len(result[1]) == 10)
    

def get_course_average_blob():
  fake_data = []
  for address in ['0x00', '0x01', '0x02', '0x03', '0x04', '0x05', '0x06', '0x07', '0x08', '0x09', '0x10', '0x11', '0x12', '0x13', '0x14', '0x15', '0x16', '0x17', '0x18', '0x19']:
    for term in [2016, 2017, 2018, 2019]:
      bodyAverage = {
        'asset': {
          'data': {
            'asset_type': 'course_average',
            'course_id': '5d7a4090b61d9af587ffa1b4',
            'degree_id': '5d7a4090b61d9af587ffa1b5',
            'faculty_id': '5d7a4090b61d9af587ffa1b6',
            'semester': 1,
            'student_address': address,
            'term': term,
            'university_id': '5d7a4090b61d9af587ffa1b7'
          }
        },
        'metadata': {
          'avg': random.randint(0, 100),
          'complete': True
        }
      }
      fake_data.append(bodyAverage)
  return fake_data