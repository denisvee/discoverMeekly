import logging
import pyodbc
import json
import os

import azure.functions as func

def average_analysis():
    # Call spotify API and return average feature values for buckets

def get_uris():
    uris = []
    buckets = []
    server = 'discoverweeklys.database.windows.net'
    database = 'discoverWeeklys'
    username = os.environ['AZURE_USER']
    password = os.environ['AZURE_PW']
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+',1433'+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM DiscoverWeeklyUris')
    for row in cursor.fetchall():
        uris.append(row[0])
    for i in range(0, len(uris), 30):
             buckets.append(uris[i:i + 30])
    return buckets

def main(req: func.HttpRequest) -> func.HttpResponse:
    uris = []
    logging.info('Python HTTP trigger function processed a request.')
    if (req.params.get('req_type') == 'get_uris'):
        return func.HttpResponse(
            status_code = 200,
            body = json.dumps(get_uris())
        )
    elif (req.params.get('req_type') == 'song_analysis'):
        return func.HttpResponse(
            body = json.dumps(song_analysis())
        )
    else:
        return func.HttpResponse(
            body = "Check req_type parameter",
            status_code = 404
        ) 
    return func.HttpResponse(
        status_code = 200
    )