#from home.dash_apps.finished_apps.Datencollection import opc
import _thread
import time
import datetime
from opcua import Client
#from home import models
#from . import Influxdb
from .Datamodel import DataModel
from .AbstractClass import Collection



class Opc(Collection):
    def __init__(self,ServerName,NodeId,VariableName):
        self.protocol='opc'
        self.ServerName=ServerName
        self.NodeId=NodeId
        self.VariableName=VariableName

    def GetData(self):
        if(self.ServerName==''):
            self.ServerName= 'opc.tcp://localhost:48010'
        if(self.NodeId ==''):
            self.NodeID = "ns=2;s=Demo.Dynamic.Scalar.Double"
        client = Client(self.ServerName)

        try:
            client.connect()
            opc = DataModel()
            val = client.get_node(self.NodeId)
            opc.name = self.VariableName
            opc.value = val.get_value()
            opc.status = val.get_data_value().StatusCode
            opc.time = val.get_data_value().SourceTimestamp
            opc.typ = val.get_data_value().Value.VariantType
            return opc
        except Exception:
            print(Exception.args)
        finally:
            client.disconnect()

if __name__ == "__main__":
    node = "ns=2;s=Demo.Dynamic.Scalar.Double"
    ServerName = 'opc.tcp://localhost:48010'
    temperatureNode = Opc(ServerName,node,'temperature')
    temperature = temperatureNode.GetData()
    print(temperature.value)
