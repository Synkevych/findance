from datetime import datetime
import constants as keys
import psycopg2
import re

today = datetime.now()

def push_to_db(query, record_to_insert):
  try:
    #establishing the connection
    connection = psycopg2.connect(database=keys.DB_NAME, user=keys.DB_USER,
                                  password=keys.DB_PASSWORD, host=keys.DB_HOST, port='5432')
    #Creating a cursor object using the cursor() method
    cursor = connection.cursor()

    #Executing an SQL function using the execute() method
    cursor.execute(query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully")

  except (Exception, psycopg2.Error) as error:
      print("Failed to insert record into table", error)

  finally:
      # closing database connection.
      if connection:
          cursor.close()
          connection.close()
          print("PostgreSQL connection is closed")


def get_expenses_by_month(user_id, start_date, end_date):
  try:
    connection = psycopg2.connect(database=keys.DB_NAME, user=keys.DB_USER,
                                  password=keys.DB_PASSWORD, host=keys.DB_HOST, port='5432')
    cursor = connection.cursor()

    get_expenses_query = """ select spent_at, amount, categories from expenses where user_id = %s AND spent_at BETWEEN %s AND %s order by spent_at desc limit 20; """
    record_to_insert = (user_id, start_date, end_date)
    cursor.execute(get_expenses_query, record_to_insert)

    connection.commit()
    return cursor.fetchall()

  except (Exception, psycopg2.Error) as error:
      print("Failed to execute SQL", error)

  finally:
      # closing database connection.
      if connection:
          cursor.close()
          connection.close()
          print("PostgreSQL connection is closed")


def get_incomes_by_month(user_id, start_date, end_date):
  try:
    connection = psycopg2.connect(database=keys.DB_NAME, user=keys.DB_USER,
                                  password=keys.DB_PASSWORD, host=keys.DB_HOST, port='5432')
    cursor = connection.cursor()

    get_expenses_query = """ select earned_at,amount,categories from incomes where user_id = %s AND earned_at BETWEEN %s AND %s order by earned_at desc limit 20; """
    record_to_insert = (user_id, start_date, end_date)
    cursor.execute(get_expenses_query, record_to_insert)

    connection.commit()
    return cursor.fetchall()

  except (Exception, psycopg2.Error) as error:
      print("Failed to execute SQL", error)

  finally:
      # closing database connection.
      if connection:
          cursor.close()
          connection.close()
          print("PostgreSQL connection is closed")


def prepare_args(user_id, created_at, operation_type, amount, categories, comment=''):
  # example of response "20/12/2022 + 200 shop,hat"
  categories = categories.split(',')
  amount = float(amount)

  if ord(operation_type) == 43:
    operation_name = "income"
    query = """ INSERT INTO incomes (USER_ID, EARNED_AT, AMOUNT, CATEGORIES, COMMENT) VALUES (%s,%s,%s,%s,%s) """
    record_to_insert = (user_id, created_at, amount, categories, comment)
  elif ord(operation_type) == 45:
    operation_name = "expense"
    query = """ INSERT INTO expenses (USER_ID, SPENT_AT, AMOUNT, CATEGORIES, COMMENT) VALUES (%s,%s,%s,%s,%s) """
    record_to_insert = (user_id, created_at, amount, categories, comment)
  else:
    return "Can\'t save this entry, incorrect message."

  push_to_db(query, record_to_insert)

  return "New <b>" + operation_name + " ???" + str(int(amount)) + "</b> with category <b>" + ", ".join(categories) + "</b> successfully added."

def sample_responses(input_text, user_id):
  user_message = str(input_text).lower()
  re_date = "((\d{1,2})+\/+(\d{1,2})+\/+(\d{4})+\s)"
  re_type = "([\-|\+])+\s"
  re_amount = "+((\d{1,})+(([\.]{1,})+[\d]{1})?)+\s"
  re_category = "+([\w,-]{1,})"
  re_comment = "+\s+([\w]{1,})"
# comment = re.findall(r"\"(.*?)\"", user_message)
  if user_message in ("hello", "hi", "????????????"):
    return "Hey! How's it going?"

  if re.match(re_date+re_type+re_amount+re_category+re_comment, user_message):
    created_at, operation_type, amount, categories, comment = re.split("\s", user_message, 4)
    created_at = datetime.strptime(created_at, '%d/%m/%Y')
    return prepare_args(user_id, created_at, operation_type, amount, categories, comment)

  if re.match(re_date+re_type+re_amount+re_category, user_message):
    created_at, operation_type, amount, categories = re.split("\s", user_message, 3)
    created_at = datetime.strptime(created_at, '%d/%m/%Y')
    return prepare_args(user_id, created_at, operation_type, amount, categories)

  if re.match(re_type+re_amount+re_category+re_comment, user_message):
    operation_type, amount, categories, comment = re.split("\s", user_message, 3)
    return prepare_args(user_id, today, operation_type, amount, categories, comment)

  if re.match(re_type+re_amount+re_category, user_message):
    operation_type, amount, categories = re.split("\s", user_message, 2)
    return prepare_args(user_id, today, operation_type, amount, categories)

  return "I don\'t understand your message, \"" + input_text + "\".\nType /help to get more info."
