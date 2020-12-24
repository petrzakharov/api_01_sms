import logging
import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client


def get_status(user_id):
    """
    Возвращает статус пользователя ВК.
    """
    params = {'user_ids': user_id,
              'v': '5.92',
              'fields': 'online',
              'access_token': os.getenv('VK_TOKEN')
              }
    url_with_method = 'https://api.vk.com/method/users.get'
    result = requests.post(url_with_method, params=params)
    status = result.json()['response'][0].get('online', 0)
    logging.info(f'user_id: {user_id}, status: {status}')
    return status


def sms_sender(sms_text):
    """
    Отправляет смс если статус соответствует условиям.
    Возвращает sid отправленного сообщения из Twilio.
    """
    client = Client(os.getenv("TW_SID"), os.getenv("TW_TOKEN"))
    message = client.messages.create(
        to=os.getenv('NUMBER_TO'),
        from_=os.getenv('NUMBER_FROM'),
        body=sms_text)
    return message.sid


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO, filename='info.log',
                        format='%(asctime)s %(levelname)s:%(message)s')
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id):
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
