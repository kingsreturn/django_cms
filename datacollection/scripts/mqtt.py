import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from queue import Queue
from django.core.cache import cache
import json
#import numpy as np
#from .Influxdb import Influxdb
import time

class Mqtt():
    def __init__(self,address,server,port):
        self.protocol='mqtt'
        self.server = '8.140.157.208'
        self.port=8083
        self.address=address
        self.client = mqtt.Client(self.address,transport="websockets")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.SubscribeData
        self.client.on_disconnect=self.on_disconnect()
        self.Data=list(range(0,100,1))
        self.interval=3
        self.count = 0
        #self.influxdb = Influxdb()
        #self.influxdb.ConnnectDatabase()
        cache.set(address, self.Data, 30)
        cache.set(self.address + '/value', 1, 30)
        self.client.connect(self.server, self.port, 60)
        self.client.subscribe(address, 0)
        self.client.loop_start()

    # connect broker
    def ConnectBroker(self):
        result = self.client.connect(self.address,self.port,60)
        return result

    # call back function when new message publish to topic
    def SubscribeData(self,client, userdata, msg):
        self.count+=1
        value = float(msg.payload.decode("utf-8"))
        if self.count==10:
            self.count=0
            del self.Data[0:10]
            cache.set(self.address,self.Data,10)
            cache.set(self.address+'/value',value,10)
            #print(self.Data[0:40])
            #self.StoreData(self.Data[0:10])
        self.Data.append(round(value,3))
        #print(self.Data[0:40])
        return str(msg.payload.decode("utf-8"))

    # call back function when disconnected to broker
    def on_disconnect(self):
        self.client.loop_stop()

    # call back function when connected to broker
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def StoreData(self,dataset):
        try:
            self.influxdb.WriteDataset('sensor',self.protocol,self.address,dataset)
        except:
            print(self.address + ' failed to write to Database!')

def on_publish(client, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

if __name__ == '__main__':
    topic1= "/test/sin"
    topic2= "/test/cos"
    client1 = Mqtt("/test/sin","8.140.157.208", 8083)
    client2 = Mqtt("/test/cos","8.140.157.208", 8083)
    time.sleep(30)
    client1.client.disconnect()
