
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

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):

                    sender_id = messaging_event["sender"]["id"]

                    if messaging_event["message"].get("text"):
                        message_text = messaging_event["message"]["text"]

                        send_typing_on(sender_id)

                        flow.execute_method(sender_id, message_text, ACCESS_TOKEN)

                    else:
                        flow.execute_method(sender_id, "error", ACCESS_TOKEN)

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):

                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["postback"]["title"]
                    return_id = messaging_event["postback"]["payload"]

                    send_typing_on(sender_id)

                    flow.execute_method(sender_id, message_text, ACCESS_TOKEN)

    return "ok", 200


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
