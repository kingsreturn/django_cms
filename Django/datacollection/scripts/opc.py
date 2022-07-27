import _thread
import time
import datetime
from opcua import Client
import time
import datetime
from django.core.cache import cache
from Influxdb import Influxdb


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    def __init__(self,name):
        self.count=0
        self.dataset=list(range(0,100,1))
        self.influxdb = Influxdb()
        self.influxdb.ConnnectDatabase()
        self.name = name
        self.temp = list(range(0,100,1))

    def datachange_notification(self, node, val, data):
        self.count+=1
        self.temp.append(val)
        print(val)
        if self.count == 20:
            self.count = 0
            del self.dataset[0:20]
            self.dataset.extend(self.temp)
            #cache.set(self.name,self.dataset,15)
            #self.influxdb.WriteDataset('sensor','opc',self.name,self.temp)
            print(self.temp)
            self.temp = []

    def event_notification(self, event):
        print("Python: New event", event)

class Opc():
    def __init__(self,server,VariableName,node):
        self.protocol='opc'
        self.server=server
        self.VariableName = VariableName
        self.node = node
        status = self.ConnectServer()
        print(status)
        self.SubscribeData(self.node)
        #if status:
        #    self.SubscribeData(self.node)
        #else:
         #   print('Not connected to the server {}'.format(self.server))


    def ConnectServer(self):
        try:
            self.client = Client(self.server)
            self.client.connect()
            return True
        except:
            print('Failed to connect to the server: {}!'.format(self.server))
            return False


    def SubscribeData(self,node):
        Node = self.client.get_node(node)

        # subscribing to a variable node
        handler = SubHandler(self.VariableName)
        self.sub = self.client.create_subscription(3600, handler)
        print('Subscription started!')
        self.handle = self.sub.subscribe_data_change(Node)

    def StoreData(self,inlfuxdb:Influxdb,dataset):
        try:
            inlfuxdb.WriteDataset('sensor',self.protocol,self.VariableName,dataset)
        except Exception:
            print(Exception.args())
            print(self.VariableName + ' failed to write to Database!')

    def disconnect_server(self):
        self.sub.unsubscribe(self.handle)
        self.sub.delete()
        self.client.disconnect()



if __name__ == "__main__":
    node = "ns=2;s=Demo.Static.Scalar.Double"
    #node = "ns=2;s=Demo.Dynamic.Scalar.Double"
    ServerName = 'opc.tcp://localhost:48010'
    variable = 'double'
    opc = Opc(ServerName,variable,node)
    #time.sleep(15)
    #opc.disconnect_server()
