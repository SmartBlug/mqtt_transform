#!/usr/bin/python3

import paho.mqtt.client as paho
from datetime import datetime
import json
import os
import sys

import MQTTPattern

#def on_subscribe(client, userdata, mid, granted_qos):
#  print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
  global conf
  #print(conf)
  #print()
  m_decode=str(msg.payload.decode("utf-8","ignore"))
  data = json.loads(m_decode)
  #print(type(data))
  if type(data) is int:
    data = {}
  for conf in confs:
    if MQTTPattern.matches(conf["topic"],msg.topic):
      # check all actions
      for action in conf['actions']:
        # check if action is enabled
        enabled = True
        if 'enabled' in action:
          enabled = action['enabled']
        if enabled:
          # if enabled, add topic en exec action
          action['topic']=conf['topic']
          try:
            exec(action['action']+"(action,data,msg)")
          except:
            e = sys.exc_info()[0]
            print(e)
            pass

      #exec("addTimestamp(action,data)")
      #print(data)
  #m_decode=str(msg.payload.decode("utf-8","ignore"))
  #data = json.loads(m_decode)
  #now = datetime.now() 
  #data['time'] = now.strftime("%m/%d/%Y - %H:%M:%S")    
  #data['ts'] = datetime.timestamp(now)
  print(">>"+msg.topic[2:]+" "+str(msg.qos)+" "+str(data))
  #print(msg.topic[2:])
  client.publish(msg.topic[2:],json.dumps(data))

def addTimestamp(action,data,msg):
  #print("addTimestamp",action,data)
  now = datetime.now() 
  for key in action['data']:
    #print("#"+key)
    if action['data'][key]:
      if key == 'time':
        data['time'] = now.strftime("%m/%d/%Y - %H:%M:%S")    
      elif key == 'ts':
        data['ts'] = datetime.timestamp(now)

def rename(action,data,msg):
  #print("rename")
  for key in action['data']:
    if key in data:
      data[action['data'][key]] = data[key]
      del data[key]

def setValue(action,data,msg):
  global variables
  #print("setValue",action,msg.topic)
  content = MQTTPattern.extract(action["topic"],msg.topic)
  #print(content)
  if not 'id' in content:
    content['id'] = action['id']
  ldict = { 'data':data }
  if content['id'] in variables:
    ldict['value'] = variables[content['id']]
  else:
    ldict['value'] = 0
  for onelambda in action['lambdas']:
    exec(onelambda,globals(),ldict)
    #exec(action['lambda'],globals(),ldict)
  variables[content['id']] = ldict['value']
  #if 'output' in action:
  #  data[action['output']] = ldict['value']

variables = {}
confs = []
for file in os.listdir("conf"):
  if file.endswith(".json"):
    with open('conf/'+file) as f:
      confs.append(json.load(f))

#print(conf)
# globalsParameter = {}
# localsParameter = {'action': {"coucou":1}, 'data': {"datac":1}}
# exec("addTimestamp(conf)",globals(),locals())

# pattern = "/$/#"
# topic = "/$/quadro/status"
# print(MQTTPattern.matches(pattern, topic))

client = paho.Client()
#client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("mqtt", 1883)
client.subscribe("$/#")#, qos=1)
client.loop_forever()

pattern = "device/+id/#data"
topic = "device/fitbit/heartrate/rate/bpm"

print(MQTTPattern.exec(pattern, topic))