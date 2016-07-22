from flask import Flask, request
import json
import requests

from wit import Wit
from googlevoice import Voice
import BeautifulSoup
import time

from bstest6_3 import foodSites


app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAXOE1KsIx0BAGgLHCjdlINT2kBtHEL4iKGuAc7Gx5hjAO8uTsHvYoQymjRRjuezdi3NixXEPgOiDKCwS3tS5JpTVmkit1RjbNZBCRJA4xYIkeKglgPDtbi6futpntkEfq5vIzRSKycEHr5ZACuU7vN1ZAOBOJ29qy67sw76AZDZD'
@app.route('/', methods=['GET'])
def handle_verification():
  print "Handling Verification."
  if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
    print "Verification successful!"
    return request.args.get('hub.challenge', '')
  else:
    print "Verification failed!"
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
  print "Handling Messages"
  payload = request.get_data()
  print payload
  for sender, textmsg in messaging_events(payload):
    print "Incoming from %s: %s" % (sender, textmsg)
    resp = client.message(textmsg)
    resp = resp[u'entities']
    resp = resp[u'intent']
    resp = resp[0]
    print ("Response type is.... "+resp[u'value'])
    if u'value' in resp:
      if resp[u'value'] == "grocery":
        resp = client.run_actions('my-user-session-42',textmsg, context0)
        print("This resp grocery ")
        print (resp)
        while('foodList' not in resp):
          resp = client.run_actions('my-user-session-42',textmsg, context0)
          print ("This resp ")
          print(resp)
          message = str(resp['foodList'])
        send_message(PAT, sender, message)
         
      elif resp[u'value'] == "greetings":
        resp = client.converse('my-user-session-42',textmsg, context0)
        print("This resp greetings ")
        print (resp)
        while('msg' not in resp):
          resp = client.converse('my-user-session-42',textmsg, context0)
          print ("This resp HERE ")
          print(resp)
          message = str(resp["msg"])
        send_message(PAT, sender, message)
      elif resp[u'value'] == "weather":
        #resp = client.run_actions('my-user-session-42',textmsg, context0)
        print("This resp weather ")
        #print (resp)
        #while('foodList' not in resp):
        #    resp = client.run_actions('my-user-session-42',textmsg, context0)
        #    print ("This resp ")
        #    print(resp)
        #voice.send_sms(msg[u'from'],str(resp['forecast']))
        message = "weather"
        send_message(PAT, sender, message)
      else:
        print("Else")
        message = "else"
        send_message(PAT, sender, message)
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text

def merge():
    return 0

def error():
    return 0

def say(id, dict, response):
    print ("id " +id)
    print (dict)
    print ("respo "+response)
    return response
    
def send(request, response):
    print(response['text'])

def my_action(request):
    print('Received from user...', request['text'])

def get_forecast(request):
    context = request['context']
    entities = request['entities']

    loc = first_entity_value(entities, 'location')
    if loc:
        context['forecast'] = 'sunny'
    else:
        context['missingLocation'] = True
        if context.get('forecast') is not None:
            del context['forecast']

    return context

def get_cooking(ent, cont):
    print(cont)
    print (ent)
    context = cont
    cook = foodSites()
    cook.initList()
    context['foodList'] = cook.getIngred()
    return context
    

actions = {
    'send': send,
    'getForecast': get_forecast,
    'say': say,
    'merge': merge,
    'error': error,
    "getCooking": get_cooking,
    'my_action': my_action,
}

#server access
client = Wit(access_token="ZNJWKAFJBJI4UXBMTL2O4YW2RNKOSABS", actions=actions)

#client token
#client = Wit(access_token="2F5GRMKTGCRTVHIAZO7HXY64LFFSVYWL", actions=actions)
#client.interactive()


if __name__ == '__main__':
  app.run()


