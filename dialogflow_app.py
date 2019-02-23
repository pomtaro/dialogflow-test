
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

    print('intent')
    print(data['queryResult']['intent']['displayName'])

    return "ok", 200


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
