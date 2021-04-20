import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from AbstractClass import Collection
from Datamodel import DataModel


class mqtt(Collection):
    def __init__(self):
        self.protocol='mqtt'
        self.server = 'localhoast'
        self.port=8083
        self.address="testtopic/#"
        self.client = mqtt.Client(transport="websockets")
        self.client.on_connect = on_connect
        self.client.on_message = on_message

    def ConnectBroker(self):
        result = self.client.connect(self.address,self.port,60)
        return result

    def GetData(self):

        pass

# 连接的回调函数
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("$SYS/#")


# 收到消息的回调函数
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
    print(string)


client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 8083, 60)
client.subscribe("testtopic/#", 0)
client.loop_forever()
#msg = subscribe.simple("testtopic/#", hostname="localhost:8083")
#print('success')
#print(f"{msg.topic} {msg.payload}")
