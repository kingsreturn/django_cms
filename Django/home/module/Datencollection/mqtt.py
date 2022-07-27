import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
#from AbstractClass import Collection
#from Datamodel import DataModel
from queue import Queue
from django.core.cache import cache
import json
#import numpy as np

class Mqtt():
    def __init__(self,address):
        self.protocol='mqtt'
        self.server = '8.140.157.208'
        self.port=8083
        self.address=address
        self.client = mqtt.Client(transport="websockets")
        self.client.on_connect = on_connect
        self.client.on_message = self.on_message
        self.Data=list(range(0,100,1))
        self.interval=3
        self.count = 0
        cache.set(address, self.Data, 30)
        cache.set(self.address + '/value', 1, 30)


    def ConnectBroker(self):
        result = self.client.connect(self.address,self.port,60)
        return result

    def GetData(self):
        pass

    def on_message(self,client, userdata, msg):
        times = self.interval / 0.1
        self.count+=1

        Drehmoment = float(msg.payload.decode("utf-8"))
        if self.count==30:
            self.count=0
            del self.Data[0:30]
            cache.set(self.address,self.Data,10)
            print(self.address,' is updated!')
            #print(self.Data)
            #self.Data.clear()
            cache.set(self.address+'/value',Drehmoment,10)

        self.Data.append(Drehmoment)
        #self.StoreDataPoint(Drehmoment, '', 'Drehmoment')
        #print(self.Data)
        return str(msg.payload.decode("utf-8"))

# 连接的回调函数
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    #client.subscribe("$SYS/#")


def on_publish(client, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
    print(string)

if __name__ == '__main__':
    mqtt_client = Mqtt("/test/sin")
    mqtt_client.client.connect("8.140.157.208", 8083, 60)
    mqtt_client.client.subscribe("/test/sin", 0)
    mqtt_client.client.loop_forever()


    #client = mqtt.Client(transport="websockets")
    #client.on_connect = on_connect
    #client.on_message = on_message
    #client.connect("8.140.157.208", 8083, 60)
    #client.subscribe("/test/motor", 0)
    #client.loop_forever()
    #msg = subscribe.simple("testtopic/#", hostname="localhost:8083")
    #print('success')
    #print(f"{msg.topic} {msg.payload}")
