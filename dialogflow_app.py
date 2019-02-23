
import os
import sys
import json
import time
import requests
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    data = request.get_json()
    print('***** post data *****')
    print(data)

    # intentの確認
    print('intent')
    intent = data['queryResult']['intent']['displayName']
    print(intent)

    # parameterの確認、Entity
    print('entity')
    entity_building = data['queryResult']['parameters']['building']
    print(entity_building)

    # sender id
    sender_id = data['originalDetectIntentRequest']['payload']['data']['sender']['id']

    # send message
    text = 'intent : {}\n' \
           'entity'.format(
                intent,
                entity_building)

    send_message(sender_id, text, ACCESS_TOKEN)

    return "ok", 200


def send_message(recipient_id, text, access_token):

    params = {
        "access_token": access_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
