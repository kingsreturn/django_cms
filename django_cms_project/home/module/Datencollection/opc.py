#from home.dash_apps.finished_apps.Datencollection import opc
import _thread
import time
import datetime
from opcua import Client
#from home import models
#from . import Influxdb
from .Datamodel import DataModel
from .AbstractClass import Collection
import time
import datetime

class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    def __init__(self):
        self.count=0
        self.data=[]

    def datachange_notification(self, node, val, data):
        self.count+=1

        self.data.append(val)
        if self.count == 10:
            self.count = 0
            print(self.data)
            self.data.clear()
        #print("Python: New data change event", node, val,datetime.datetime.now())

    def event_notification(self, event):
        print("Python: New event", event)

class Opc(Collection):
    def __init__(self,ServerName):
        self.protocol='opc'
        self.ServerName=ServerName
        self.client = Client(self.ServerName)
        self.client.connect()
        #self.NodeId=NodeId
        #self.VariableName=VariableName

    def GetData(self,node):
        if(self.ServerName==''):
            self.ServerName= 'opc.tcp://localhost:48010'
        if(self.NodeId ==''):
            self.NodeId= "ns=2;s=Demo.Dynamic.Scalar.Double"
        client = Client(self.ServerName)

        try:
            client.connect()
            opc = DataModel()
            val = client.get_node(self.NodeId)
            #opc.name = self.VariableName
            opc.value = val.get_value()
            opc.status = val.get_data_value().StatusCode
            opc.time = val.get_data_value().SourceTimestamp
            opc.typ = val.get_data_value().Value.VariantType
            return opc
        except Exception:
            print(Exception.args)
        finally:
            client.disconnect()

    def GetDataset(self,interval,node):
        intial = 0
        data =[]
        while intial < interval:
            data.append(self.GetData(node))
            time.sleep(1)
            intial+=1
        return data

    def Subscribe_Node(self,node):
        Node = self.client.get_node(node)

        # subscribing to a variable node
        handler = SubHandler()
        sub = self.client.create_subscription(500, handler)
        print('Subscription started!')
        handle = sub.subscribe_data_change(Node)
        #time.sleep(0.1)

        # we can also subscribe to events from server
        #sub.subscribe_events()





if __name__ == "__main__":
    node = "ns=2;s=Demo.Dynamic.Scalar.Double"
    ServerName = 'opc.tcp://localhost:48010'
    opc = Opc(ServerName)
    opc.Subscribe_Node(node)
    #temperature = opc.GetData(node)
    #print(temperature.value)
