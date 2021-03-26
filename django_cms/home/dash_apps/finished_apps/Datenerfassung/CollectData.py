#from home.dash_apps.finished_apps.Datenerfassung import opc
import _thread
import time
from opcua import Client

class SensorData:
    def __init__(self, protocol="opc", server ='',address=''):
        # self.name是成员变量，name是形参、局部变量
        self.protocol = protocol
        self.server = server
        self.address = address
        self.sampling = True
        self.data = []

    def StoreData(self):
        #store data to Database
        pass

    def getData(self):
        # if we use opc ua then return the data from opcua
        # otherweise we get data from other ways
        # other ways can be integrated afterwards
        if(self.protocol == 'opc'):
            return Opc.GetData(self.server,self.address)

    # Constantly read Data into Dataset, return the Dataset when the function is called
    def ConstantlyReadData(self):
        _thread.start_new_thread(self.DataSampling(self.data,1))
        return self.data

    # constant data sampling
    def DataSampling(self,data:list,interval:int):
        while(self.sampling):
            data.append(self.getData())
            time.sleep(interval)

class Opc(dict):
    #def __init__(self,Server,Node):
        #SensorData.__init__('opc',Server,Node)
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def GetData(ServerName,NodeID):
        if(ServerName=='' or NodeID ==''):
            ServerName= 'opc.tcp://localhost:48010'
            NodeID = "ns=2;s=Demo.Dynamic.Scalar.Double"
        client = Client(ServerName)
        try:
            client.connect()
            opc = Opc()
            val = client.get_node(NodeID)
            opc.value = val.get_value()
            opc.status = val.get_data_value().StatusCode
            opc.time = val.get_data_value().SourceTimestamp
            opc.typ = val.get_data_value().Value.VariantType
            return opc.value
        except Exception:
            print(Exception.args)
        finally:
            client.disconnect()

if __name__ == "__main__":
    node = "ns=2;s=Demo.Dynamic.Scalar.Double"
    ServerName = 'opc.tcp://localhost:48010'
    NodeObject = SensorData('opc',ServerName,node)
    opcObject = NodeObject.getData()