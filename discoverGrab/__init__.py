import datetime
import logging
import spotify_extract
import db_helper

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    songs = {}
    # Authenticate with spotify
    # Retry refresh token
    # Get songs and create table
    
    spotify_extract.get_songs()
    db_helper.new_table()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)