import mysql.connector
from bin.config_utils import DBDATA as DB
from bin.appslib import handle_error
def connect_to_database(queryA, userA=DB['user'], passwordA=DB['pass'], hostA=DB['host'], databaseA=DB['base']):
    """Łączy się z bazą danych i zwraca List"""
    try:
        polaczenie_DB = mysql.connector.connect(
            user=userA,
            password=passwordA,
            host=hostA,
            database=databaseA)
        cursor = polaczenie_DB.cursor()
        query = queryA # 'SELECT id, user, haslo, created FROM users_main'

        cursor.execute(query)
        export_list = []
        for data in cursor:
            export_list.append(data)

        polaczenie_DB.commit()
        polaczenie_DB.close()
    except Exception as e:
        handle_error(e)
    return export_list

def insert_to_database(queryA, queryB, userA=DB['user'], passwordA=DB['pass'], hostA=DB['host'], databaseA=DB['base']):
    """Łączy się z bazą danych i robi insert"""
    try:
        polaczenie_DB = mysql.connector.connect(
            user=userA,
            password=passwordA,
            host=hostA,
            database=databaseA)
        cursor = polaczenie_DB.cursor()
        query = queryA  # 'INSERT INTO your_table (column1, column2, datetime_column) VALUES (%s, %s, %s)'
        values = queryB  # ("value1", "value2", datetime_value)
        
        cursor.execute(query, values)
        
        polaczenie_DB.commit()
        polaczenie_DB.close()
    except Exception as e:
        handle_error(e)
    return True

def delete_row_from_database(queryA, queryB, userA=DB['user'], passwordA=DB['pass'], hostA=DB['host'], databaseA=DB['base']):
    try:
        polaczenie_DB = mysql.connector.connect(
            user=userA,
            password=passwordA,
            host=hostA,
            database=databaseA)
        cursor = polaczenie_DB.cursor()
        query = queryA  # 'DELETE FROM twoja_tabela WHERE kolumna1 = %s AND kolumna2 = %s AND kolumna_daty = %s;'
        values = queryB  # ("value1", "value2", datetime_value)
        
        cursor.execute(query, values)
        
        polaczenie_DB.commit()
        polaczenie_DB.close()
    except Exception as e:
        handle_error(e)

