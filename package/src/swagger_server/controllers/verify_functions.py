import pandas as pd

def _verify_degree(filename, student_id, degree_code):
  data = pd.read_csv(filename, dtype = {'student id': 'string', 'degree code': 'string', 'complete': 'bool'})
  data_filtered = data[(data['student id'] == student_id) & (data['degree code'] == degree_code)]
  if data_filtered.empty:
    return False
  else:
    return bool(data_filtered.iloc[0]['complete'])
