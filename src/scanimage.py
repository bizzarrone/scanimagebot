#!/usr/bin/env python3.7
"""
 Scanimage Bot
 21 Settembre 2018: creato programma (Luca Carrozza)
"""
import os
import time
import requests
import telepot

__version__ = '0.1.1'


def on_chat_message(msg):
    """
    Function used when recived a message
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        name = msg["from"]["first_name"]
        txt = msg['text']

        if txt.startswith('/scan'):
            SCANIMAGE.sendMessage(chat_id, 'Eseguo scansione')
            os.system("scanimage --resolution 150 -y 297 -x 215 --format jpeg -p > scan.jpg")
            f = open( "scan.jpg", 'rb')
     	    SCANIMAGE.sendPhoto(chat_id, f)

        elif txt.startswith('/info'):
                message = 'Ciao %s, '
                message = message + '!\nSono un bot per eseguire scansioni '
                message = message + 'tramite scanner collegato via USB.\nVersione %s '
                message = message % (name, __version__)
                SCANIMAGE.sendMessage(chat_id, message)

if __name__ == '__main__':
    TOKEN = os.environ.get('BOT_TOKEN')
    SCANIMAGE = telepot.Bot(TOKEN)
    SCANIMAGE.message_loop(on_chat_message)

    while True:
        time.sleep(10)
