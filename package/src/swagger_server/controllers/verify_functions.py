import pandas as pd

def _verify_degree(filename, student_id, degree_code):
  data = pd.read_csv(filename, header=None, names=['student_id', 'degree_code'], dtype = {'student_id': 'string', 'degree_code': 'string'})
  data_filtered = data[(data['student_id'] == student_id) & (data['degree_code'] == degree_code)]
  if data_filtered.empty:
    return False
  else:
    return True
