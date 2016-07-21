
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

context0 = {}
print("Starting bot...")
voice = Voice()
voice.login()

print("Logged in. Ready to recieve commands")
#keep bot running
while(1==1):
    voice.sms()
    for msg in extractsms(voice.sms.html):
        textmsg = str(msg[u'text'])
        resp = client.message(textmsg)
        
        resp = resp[u'entities']
        #resp = resp[u'message_body']
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
                voice.send_sms(msg[u'from'],str(resp['foodList']))
        
            elif resp[u'value'] == "greetings":
                resp = client.converse('my-user-session-42',textmsg, context0)
                print("This resp greetings ")
                print (resp)
                while('msg' not in resp):
                    resp = client.converse('my-user-session-42',textmsg, context0)
                    print ("This resp ")
                    print(resp)
                voice.send_sms(msg[u'from'],str(resp[u'msg']))

            elif resp[u'value'] == "weather":
                resp = client.run_actions('my-user-session-42',textmsg, context0)
                print("This resp weather ")
                print (resp)
                while('foodList' not in resp):
                    resp = client.run_actions('my-user-session-42',textmsg, context0)
                    print ("This resp ")
                    print(resp)
                voice.send_sms(msg[u'from'],str(resp['forecast']))
            else:
                print("Else")
                


        #resp = client.converse('my-user-session-42',textmsg, context0)
        #print("This resp ")
        #print (resp)
        #while('msg' not in resp):
         #   resp = client.converse('my-user-session-42',textmsg, context0)
          #  print ("This resp ")
           # print(resp)
        #voice.send_sms(msg[u'from'],str(resp[u'msg']))

    for message in voice.sms().messages:
        print("Deleting messages...")
        message.delete()
        
        
    time.sleep(10)
