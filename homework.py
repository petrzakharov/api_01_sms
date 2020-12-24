import os
import time
import requests

from dotenv import load_dotenv
from twilio.rest import Client


def get_status(user_id):
    """
    Возвращает статус пользователя ВК.
    """
    params = {'user_id': user_id,
              'v': '5.92',
              'fields': 'online',
              'access_token': os.getenv('VK_TOKEN')
              }
    url_with_method = 'https://api.vk.com/method/users.get'
    result = requests.post(url_with_method, params)
    status = result.json()['response'][0].get('online', 0)
    return status


def send_sms(sms_text, client, phone_data):
    """
    Отправляет смс если статус соответствует условиям.
    Возвращает sid отправленного сообщения из Twilio.
    """
    message = client.messages.create(
        to=phone_data['to'],
        from_=phone_data['from'],
        body=sms_text)
    return message.sid


if __name__ == '__main__':
    load_dotenv()
    PHONE_DATA = {'to': '+79175819649', 'from': '+12565402908'}
    client = Client(os.getenv("TW_SID"), os.getenv("TW_TOKEN"))
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!', client, PHONE_DATA)
            break
        time.sleep(5)
