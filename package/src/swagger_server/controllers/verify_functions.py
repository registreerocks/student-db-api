from os import environ as env
import mysql.connector

VERIFY_HOST = env.get("VERIFY_HOST")
VERIFY_USER = env.get("VERIFY_USER")
VERIFY_PASSWORD = env.get("VERIFY_PASSWORD")
VERIFY_DB = env.get("VERIFY_DB")



def _verify_degree(student_id, degree_code):

  connection = mysql.connector.connect(
    host=VERIFY_HOST,
    database=VERIFY_DB,
    user=VERIFY_USER,
    passwd=VERIFY_PASSWORD
  )

  if connection.is_connected():
    cursor = connection.cursor()
    query_string = "SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END AS valid FROM " + VERIFY_DB + ".student WHERE national_id = '" + student_id + "' AND degree_code = '" + degree_code + "'"
    cursor.execute(query_string)
    record = cursor.fetchone()
    if record[0]:
      return True
    else:
      return False

  else:
    return {"ERROR": "Database connection error"}, 503

