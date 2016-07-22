from flask import Flask, request
import json
import requests

app = Flask(__name__)
from wit import Wit
from googlevoice import Voice
import BeautifulSoup
import time

from bstest6_3 import foodSites

def extractsms(htmlsms) :
    """
    extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

    Output is a list of dictionaries, one per message.
    """
    msgitems = []										# accum message items here
    #	Extract all conversations by searching for a DIV with an ID at top level.
    tree = BeautifulSoup.BeautifulSoup(htmlsms)			# parse HTML into tree
    conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
    for conversation in conversations :
        #	For each conversation, extract each row, which is one SMS message.
        rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
        for row in rows :								# for all rows
            #	For each row, which is one message, extract all the fields.
            msgitem = {"id" : conversation["id"]}		# tag this message with conversation ID
            spans = row.findAll("span",attrs={"class" : True}, recursive=False)
            for span in spans :							# for all spans in row
                cl = span["class"].replace('gc-message-sms-', '')
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()	# put text in dict
            msgitems.append(msgitem)					# add msg dictionary to list
    return msgitems


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
