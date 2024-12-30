
from datetime import datetime, timedelta
from django.conf import settings
from envio_datos.src.stateful.push.core import SessionManager
import envio_datos.src.translator.session as translator_session
import logging
import asyncio


async def main_task_loop(session, payload):
    process = 1
    while True:
        process += 1
        try:
            logging.info('105: We proceed to start the execution to the Bogotá translator')
            translator_session.session_test(session, payload)
            logging.info('106: The execution of the Bogotá translator ends')
        except ConnectionError:
            logging.error("205: An unexpected error occurred in the execution of the translator.")
        await asyncio.sleep(60 * settings.ENV_REQUEST_TIME)