from src.swagger_server.controllers.verify_functions import _verify_degree

def test_verify_degree():
  filename = './mockdata/sb-mock-data.csv'
  assert(_verify_degree(filename, '60466575', 'CB001') == True)
  assert(_verify_degree(filename, '56434247', 'CB001') == False)
