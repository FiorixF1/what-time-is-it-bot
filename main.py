import urllib3
import json
import os

from logic import logic

BOT_NAME = "@WhatTimeIsItBot"
TELE_TOKEN = os.environ.get("BOT_TOKEN")
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)



# return (command, parameter)
def get_command(text):
    # "usual text message"
    if text[0] != '/':
        return ('', '')

    space = text.find(' ')
    if space == -1:
        at = text.find('@')
        if at == -1:
            # "/command"
            return (text, '')
        else:
            if text[at:] == BOT_NAME:
                # "/command@WhatTimeIsItBot"
                return (text[:at], '')
            else:
                # "/command@AnotherBot"
                return ('', '')
    else:
        command = text[:space].strip()
        parameter = text[space+1:].strip()
        at = text.find('@')
        if at == -1 or at > space:
            # "/command @my beautiful soup"
            return (command, parameter)
        else:
            if command[at:space] == BOT_NAME:
                # "/command@WhatTimeIsItBot my beautiful soup"
                return (command[:at], parameter)
            else:
                # "/command@AnotherBot my beautiful soup"
                return ('', '')



def send_message(text, chat_id):
    command, parameter = get_command(text)

    http = urllib3.PoolManager()
    if command == "/start":
        reply = "Hello! I can tell you what time it is around the world! Just send me /time followed by a country code, a country name or a city name. For example /time it or /time Italy or /time Rome"
        url = URL + "sendMessage?text={}&chat_id={}".format(reply, chat_id)
        http.request('GET', url)
    elif command == "/help":
        reply = "Send /time followed by a country code, a country name or a city name. For example /time it or /time Italy or /time Rome"
        url = URL + "sendMessage?text={}&chat_id={}".format(reply, chat_id)
        http.request('GET', url)
    elif command == "/time":
        if parameter == '':
            reply = "Send /time followed by a country code, a country name or a city name. For example /time it or /time Italy or /time Rome"
        else:
            reply = logic(parameter)
            if reply == '':
                reply = "Unknown place :("
        url = URL + "sendMessage?text={}&chat_id={}".format(reply, chat_id)
        http.request('GET', url)

def lambda_handler(event, context):
    try:
        message = json.loads(event['body'])
        chat_id = message['message']['chat']['id']
        text = message['message']['text']
        send_message(text, chat_id)
    except Exception as e:
        print(e)

    # always return 200 to Telegram !
    return {
        'statusCode': 200
    }

