import sys
sys.path.insert(0, "..")

from opcua import Client
from opcua.tools import uaread

class OpcData(dict):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

_no_value = object()
def GetDataFromOpcServer(ServerName,NodeID):
    if(ServerName==_no_value or NodeID == _no_value):
        ServerName= 'opc.tcp://localhost:48010'
        NodeID = "ns=2;s=Demo.Dynamic.Scalar.Double"
    client = Client(ServerName)
    try:
        client.connect()
        opc = OpcData()
        val = client.get_node(NodeID)
        opc.value = val.get_value()
        opc.status = val.get_data_value().StatusCode
        opc.time = val.get_data_value().SourceTimestamp
        opc.typ = val.get_data_value().Value.VariantType
        #print(val.get_value())
        return opc.value
    except SyntaxError:
        print('SyntaxError occured.')
    finally:
        #pass
        client.disconnect()

if __name__ == "__main__":
    node = "ns=2;s=Demo.Dynamic.Scalar.Double"
    ServerName = 'opc.tcp://localhost:48010'
    opcObject = GetDataFromOpcServer(ServerName=ServerName,NodeID=node)
    #client.ConnectServer('opc.tcp://localhost:48010')
    print(opcObject)
    print(opcObject.value)
