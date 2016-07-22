from flask import Flask, request
import json
import requests

app = Flask(__name__)
from wit import Wit
from googlevoice import Voice
import BeautifulSoup
import time

from bstest6_3 import foodSites

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
