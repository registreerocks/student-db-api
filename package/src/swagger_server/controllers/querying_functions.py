import math

from .global_vars import MDBC

def _query_bulk(query_list):
    responses = {}
    for item in query_list:
        if item.get('absolute'):
            responses[item.get('type_id')] = _get_top_x(item.get('x'), item.get('type'), item.get('type_id'))
        else:
            responses[item.get('type_id')] = _get_top_x_percent(item.get('x'), item.get('type'), item.get('type_id'))
    return responses

def _query_bulk_new(query_list):
    responses = {}
    for item in query_list:
        if item.get('absolute'):
            responses[item.get('type_id')] = _mongo_query(item.get('type'), item.get('type_id'), item.get('x'))
        else:
            total = _mongo_dry_run(item.get('type'), item.get('type_id'))
            n = math.ceil(item.get('x')/100 * total)
            responses[item.get('type_id')] = _mongo_query(item.get('type'), item.get('type_id'), n)
    return responses

def _get_top_x(x, _type, _id):
    averages = _retrieve_averages(_type, _id)
    if x < len(averages):
        return dict((item.pop('student_address'), item.copy()) for item in averages[:x])
    else:
        return dict((item.pop('student_address'), item.copy()) for item in averages)

def _get_top_x_percent(x, _type, _id):
    averages = _retrieve_averages(_type, _id)
    reduced_list = _x_percent(x, averages)
    return dict((item.pop('student_address'), item.copy()) for item in reduced_list)

def _retrieve_averages(_type, _id):
    files = list(MDBC.find({'asset.data.asset_type': _type + '_average', 'asset.data.' + _type + '_id': _id}))
    return _sort_averages(files)

def _sort_averages(files):
    average_dict = {}
    for f in files:
        student_address = f['asset']['data']['student_address']
        term = f['asset']['data']['term']
        if average_dict.get(student_address, {'term': 0})['term'] <= term:
            average = f['metadata']
            average['student_address'] = student_address
            average['term'] = term
            average_dict[student_address] = average
    averages = [ v for v in average_dict.values() ]
    return sorted(averages, key=lambda k: k['avg'], reverse=True)

def _x_percent(x, sorted_averages):
    y = math.ceil(x/100 * len(sorted_averages))
    return sorted_averages[:y]

def _mongo_query(_type, _id, n):
  return list(MDBC.aggregate([
    {
      "$match": {
        "asset.data.asset_type": _type + "_average",
        "asset.data.degree_id": _id
      }
    },
    {
      "$group": {
        "_id": "$asset.data.student_address",
        "max_term": {
          "$max": "$asset.data.term"
        },
        "data": {
          "$push": {
            "student_address": "$asset.data.student_address",
            "term": "$asset.data.term",
            "avg": "$metadata.avg",
            "complete": "$metadata.complete",
            "timestamp": "$metadata.timestamp",
          }
        }
      }
    },
    {
      "$project": {
        "_id": 0,
        "lastYear": {
          "$setDifference": [{
              "$map": {
                "input": "$data",
                "as": "data",
                "in": {
                  "$cond": [{
                      "$eq": ["$max_term", "$$data.term"]
                    },
                    "$$data",
                    False
                  ]
                }
              }
            },
            [False]
          ]
        }
      }
    },
    {
      "$unwind": '$lastYear'
    },
    {
      "$project": {
        "student_address": "$lastYear.student_address",
        "term": "$lastYear.term",
        "avg": "$lastYear.avg",
        "complete": "$lastYear.complete",
        "timestamp": "$lastYear.timestamp"
      }
    },
    {
      "$sort": {
        "avg": -1
      }
    },
    {
      "$limit": n
    }
  ]))

def _mongo_dry_run(_type, _id):
    return list(MDBC.aggregate([
        {
            "$match": {
                "asset.data.asset_type": _type + "_average",
                "asset.data.degree_id": _id
            }
        },
        {
            "$group": {
                "_id": "$asset.data.student_address",
                "max_term": {
                "$max": "$asset.data.term"
                },
                "data": {
                "$push": {
                    "student_address": "$asset.data.student_address",
                    "term": "$asset.data.term",
                    "avg": "$metadata.avg",
                    "complete": "$metadata.complete",
                    "timestamp": "$metadata.timestamp",
                }
                }
            }
            },
            {
            "$project": {
                "_id": 0,
                "lastYear": {
                "$setDifference": [{
                    "$map": {
                        "input": "$data",
                        "as": "data",
                        "in": {
                        "$cond": [{
                            "$eq": ["$max_term", "$$data.term"]
                            },
                            "$$data",
                            False
                        ]
                        }
                    }
                    },
                    [False]
                ]
                }
            }
            },
            {
            "$unwind": '$lastYear'
            },
            {
            "$project": {
                "student_address": "$lastYear.student_address",
                "term": "$lastYear.term",
                "avg": "$lastYear.avg",
                "complete": "$lastYear.complete",
                "timestamp": "$lastYear.timestamp"
            }
        },
        {
            "$count": "total"
        } 
    ]))[0]['total']