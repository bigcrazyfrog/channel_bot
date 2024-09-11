import schedule
import time
import configparser

from hhapi import to_file

import configparser

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from message import get_one_vacancies

# Reading Configs
config = configparser.ConfigParser()
config.read("config-sample.ini")

VACANCIES_NUMBER = int(config["Vacancies"]["number"])
CHANNEL_NAME = config["Channel"]["name"]
CHANNEL_ID = config["Channel"]["id"]

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)


async def main(phone):
    await client.start()
    print("Client Created")

    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
            
    await client.send_message(CHANNEL_ID, get_one_vacancies(CHANNEL_NAME, VACANCIES_NUMBER))


def send_to_channel():
    with client:
        client.loop.run_until_complete(main(phone))


def set_time():
    # Обновить файл
    schedule.every().day.at("10:30").do(to_file)

    # Расписание отправки 
    schedule.every().sunday.at("13:15").do(send_to_channel)
    schedule.every().monday.at("18:39").do(send_to_channel)
    schedule.every().tuesday.at("13:45").do(send_to_channel)
    schedule.every().wednesday.at("14:15").do(send_to_channel)
    schedule.every().thursday.at("15:11").do(send_to_channel)
    schedule.every().friday.at("17:03").do(send_to_channel)
    schedule.every().saturday.at("14:15").do(send_to_channel)

    # schedule.every().day.at("16:30").do(send_to_channel)
    # schedule.every().day.at("18:30").do(send_to_channel)


if __name__ == "__main__":
    to_file()
    set_time()

    while True:
        schedule.run_pending()
        time.sleep(1)
