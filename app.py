import urllib2
import os
import sys
import json
from wit import Wit

import requests
from flask import Flask, request


from chatbot_functions import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must
    # return the 'hub.challenge' value in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Facebook chat bot heroku app home page", 200


@app.route('/', methods=['POST'])
def webook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the messag
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's
                    message_text = messaging_event["message"]["text"]  # the message's text
                    ctx = {}
                    session_id = str(sender_id)
                    cnt = 0
                    while True:
                        ctx = client.run_actions(session_id, message_text, ctx)
                        send_message(sender_id, str(resp.get('msg', 'Hi')))
                        cnt +=1
                        if cnt == 3:
                            break


                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def get_response(message_ana):
    entities = message_ana.get('entities', None)
    if len(entities) >= 1:
        all_challenges = make_request()
        resp = ''
        for  obj in all_challenges.get('objects', None):
           resp += obj.get('title', None) + "<br/>"
        return resp
    else:
        return "Hello"

def make_request():
    challenges_url = 'https://devx-staaging1-frp4qj.hackerearth.com/testapi/fbbot/events/previous/?format=json'
    return json.loads(urllib2.urlopen(challenges_url).read())

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


# Wit configuration here 
actions = {
        'say': say,
        'get_events': get_events,
        'get_problems': get_problems,
        'recommend_event': recommend_event,
        'recommend_problem': recommend_problem,
        'get_all_event_types': get_all_event_types,
        'get_all_problem_tracks': get_all_problem_tracks,
        'get_all_topics': get_all_topics,
        'get_welcome_message': get_welcome_message,
        }


client = Wit(access_token='WDWTC5S65WLBPRMVLKOZO7STESWOAH7X', actions=actions)


if __name__ == '__main__':
    app.run(debug=True)
