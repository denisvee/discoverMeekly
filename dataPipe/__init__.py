import logging
import pyodbc
import os

import azure.functions as func

songs = []
buckets = []

def getUris():
    server = 'discoverweeklys.database.windows.net'
    database = 'discoverWeeklys'
    username = os.environ['AZURE_USER']
    password = os.environ['AZURE_PW']
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+',1433'+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM DiscoverWeeklyUris')
    for row in cursor.fetchall():
        songs.append(row[0])
    for i in range(0, len(songs), 30):
             buckets.append(songs[i:i + 30])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
    