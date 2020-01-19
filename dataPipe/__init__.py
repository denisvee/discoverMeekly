import logging
import pyodbc
import os

import azure.functions as func

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
    logging.info('Python HTTP trigger function processed a request.')
    uris = []

    if (req.params.get('req_type') == 'get_uris'):
        return func.HttpResponse(
            status_code = 200,
            body = json.dump(get_uris())
        )
    # elif (req.params.get('req_type') == 'song_analysis'):
    #     return song_analysis()

    return func.HttpResponse(
        status_code = 200
    )