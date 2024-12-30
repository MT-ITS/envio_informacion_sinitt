"""
This module contains all the required functions to generate a translation
"""
from distutils.log import error
import json
import logging
from datetime import datetime, timedelta
import sys
import requests
from flatten_json import flatten, unflatten_list
from django.conf import settings
import asyncio
import os
import pytz


def session_test(session, data: list) -> None:
    """stasteful session control"""
    print(f"send information of {session.typepublication}")
    if session.task.session is None:
        # try to open session
        logging.info("109: Open Session- Client Status OFF")
        try:
            res = session.request_open_session(
                settings.ENV_COUNTRY_CODE,
                settings.ENV_NATIONAL_IDENTIFIER,
                settings.FAKE_API_KEY,
            )
            logging.info(
                "118: response <"
                + str(res.status_code)
                + "> "
                + str(res.content, settings.ENCODING)
            )
        except:
            res = None
        # if the session is not opened then execute the following code
        if session.session_id is None:
            logging.info("110: Timeout or fail on openSession")
            logging.info("111: Storing publications in files...")
            # data to be stored in a file due to the server is not responding
            # the data has the unsent status
            stored_data(session.typepublication, data)
        # if the session is opened is executed the following code
        else:
            logging.info("116: Payload put data")
            # follow normal process
            res = session.request_put_data(data)
            if not res == b"{}":
                logging.info(
                    "119: response <"
                    + str(res.status_code)
                    + "> "
                    + str(res.content, settings.ENCODING)
                )
                if res.status_code == 200:
                    pass
                else:
                    stored_data(session.typepublication, data)
                    res = session.request_close_session()
                    session.session_id = None
            else:
                stored_data(session.typepublication, data)
                res = session.request_close_session()
                session.session_id = None


def stored_data(publication_type, data) -> None:
    # variable to store a list of dictionary with information about publication and status (unsent, sent)
    file_data = []

    path = f"{settings.BASE_DIR}/{settings.UNSENT_PUB_DIR}"
    print('path::::::::::::::::::')
    print(path)
    if not os.path.exists(path):
        print('create::::::::::::::::::')
        os.makedirs(path)

    # filename where are stored the publication
    unsent_publication_file = (
        f"{settings.BASE_DIR}/{settings.UNSENT_PUB_DIR}/{publication_type}-{datetime.now().date()}.json"
    )
    logging.info(
        f"MAIN_TASK_LOOP - storing publications in {unsent_publication_file}..."
    )
    try:
        with open(unsent_publication_file, encoding=settings.ENCODING) as f:
            file_data = json.load(f)
    except FileNotFoundError:
        pass
    # the current publication, stored in pub_data, is added to file_data list
    file_data = file_data + data
    # the files where are stored the unsent publication is opened as a writing file
    # the information is updated using the current file_data list
    # with open(unsent_publication_file, "wb+", encoding=settings.ENCODING) as file_sent:
    with open(unsent_publication_file, "w", encoding=settings.ENCODING) as file_sent:
        json.dump(file_data, file_sent)
    logging.info("112: The unsent publication is stored in the file")

