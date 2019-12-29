import pyodbc
import os

def new_table():
    server = 'discoverweeklys.database.windows.net'
    database = 'discoverWeeklys'
    username = os.environ['AZURE_USER']
    password = os.environ['AZURE_PW']
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM week1")
    row = cursor.fetchone()
    print(row)