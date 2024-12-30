from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from envio_datos.src.stateful.push.core import SessionManager
from envio_datos.src.stateful.push.cms import main_task_loop

from threading import Thread

import logging
import logging.config
import yaml
import asyncio


# Create your views here.
@api_view(['POST'])
def start(request, option):
    response = {'status': False}
    status_response = status.HTTP_400_BAD_REQUEST

    type_publicaicion_dict = {
        '1': settings.MEASURED_DATA_PUBLICATION,
        '2': settings.ELABORATED_DATA_PUBLICATION,
        '3': settings.SITUATION_PUBLICATION,
        '4': settings.MEASURED_SITE_TABLE_PUBLICATION,
        '5': settings.VMS_PUBLICATION,
        '6': settings.VMS_TABLE_PUBLICATION,
    }

    data = request.data
    payload = data['payload']

    session = SessionManager()
    session.typepublication = type_publicaicion_dict[option]

    Thread(target=run, args=(session, payload)).start()
    response['status'] = True
    status_response = status.HTTP_200_OK
    return Response(response, status=status_response)


def run(session, payload):
    """
    Inits the creation of the translation of a publication in a given date range
    """
    config_path = 'envio_datos/src/translator/config.yaml'
    config = yaml.safe_load(open(config_path, encoding = settings.ENCODING))
    config_log = config['log']
    logging.config.dictConfig(config_log)
    loop = asyncio.new_event_loop()
    loop.create_task(main_task_loop(session, payload))
    loop.run_forever()

    asyncio.set_event_loop(loop)