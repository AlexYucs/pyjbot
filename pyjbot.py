from flask import Flask, request
import json
import requests

import sys
import logging

from wit import Wit
import BeautifulSoup #not being used
import time

import aiml

#grocery list class
from bstest6_3 import foodSites


app = Flask(__name__)

#alice
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

#logs errors for heroku 
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

site = ''
chatAl = False

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAXQgdDXC2kBAI2zLHJSZA6Aapz1iPCodArxZAU2lDZAmt7IYrKgewl6a6OWvsCRx0nv6hvhrAiIPmhUKBffeJ9V7YGDoZBENixzZCPqpEM3OvZBcBdZCori4RtBC5nVdJZA6mfLgoIOruJE96Xvo0ZBqIPu6OXzBwbCxVzOE8mcoyAZDZD'

#verify
@app.route('/', methods=['GET'])
def handle_verification():
  print "Handling Verification."
  if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
    print "Verification successful!"
    return request.args.get('hub.challenge', '')
  else:
    print "Verification failed!"
    return 'Error, wrong validation token'


#messaging
@app.route('/', methods=['POST'])
def handle_messages():
  global site
  context0 = {}
  count = 0
  global chatAl
  print ("current " +chatAl)
  print "Handling Messages"
  payload = request.get_data()
  print payload
  for sender, message in messaging_events(payload):
    if chatAl:
      print "Incoming from %s: %s" % (sender, message)
      print("Alice bot")
      if message == "bye":
        chatAl =False
      m1 = kernel.respond(message)
    
      print m1
      print("Trying to send...")
      send_message(PAT, sender, m1)
      print("Probably sent")
  else:
    print "Incoming from %s: %s" % (sender, message)
    print type(message)
    resp = client.message(message)
    resp = resp[u'entities']
    resp = resp[u'intent']
    resp = resp[0]
    print ("Response type is.... "+resp[u'value'])
      
    #id type of response and run correct method
    if u'value' in resp:
      if resp[u'value'] == "grocery":
        message = get_cooking()
        send_message(PAT, sender, message)
        send_message(PAT, sender, site) 
          
      elif resp[u'value'] == "xkcd":
        message = "http://xkcd.com/"
        send_message(PAT, sender, message)
          
      elif resp[u'value'] == "greetings":
        print("This resp greetings RIGHT HERE")
        resp = client.converse('my-user-session-42',message, context0)
        print("This resp greetings ")
        print (resp)
        while('msg' not in resp):
          resp = client.converse('my-user-session-42',message, context0)
          print ("This resp HERE ")
          print(resp)
          
        print("the msg is "+resp['msg'])
        message = str(resp["msg"])
        print("Trying to send...")
        send_message(PAT, sender, message)
        print("Probably sent")
          
      elif resp[u'value'] == "talk":
        chatAl =True
        send_message(PAT, sender, "Okay, what's up?")
    
          #not working atm
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
        resp = client.converse('my-user-session-42',message, context0)
        while('msg' not in resp and count <=10):
          resp = client.converse('my-user-session-42',message, context0)
          print ("This resp HERE ")
          print(resp)
            
        print("the msg is "+resp['msg'])
        message = str(resp["msg"])
        print("Trying to send...")
        send_message(PAT, sender, message)
  return "ok"

#Sorts messages
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

#Send the message. Limited to 320 char
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

#wit ai method not implemented
def merge():
    return 0

#wit ai method not implemented (important probably)
def error():
    return 0

#wit ai method works
def say(id, dict, response):
    print ("id " +id)
    print (dict)
    print ("respo "+response)
    return response
    
def send(request, response):
    print(response['text'])

def my_action(request):
    print('Received from user...', request['text'])

#gotta use a weather module
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

#works fine so far. Can't run from wit.ai
def get_cooking():
    print("Inside grocery")
    global site
    context = ""
    cook = foodSites()
    cook.initList()
    context= cook.getIngred()
    site = cook.getSites()
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


if __name__ == '__main__':
  app.run()
