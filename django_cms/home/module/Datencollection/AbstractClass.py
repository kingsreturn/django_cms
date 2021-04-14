from abc import abstractmethod,ABCMeta
from .Influxdb import Influxdb


class Collection(metaclass=ABCMeta):
    def __init__(self):
        # self.name是成员变量，name是形参、局部变量
        self.protocol = ''
        self.server = ''
        self.address = ''
        self.sampling = True
        self.data = []

    @abstractmethod
    def GetData(self):
        # The GetData methode will be realisiert in subclass
        # Every subclass has such method
        pass

    def StoreDataPoint(self,value,time,VariableName):
        influxdb = Influxdb()
        influxdb.WriteDataPoint(self.protocol,VariableName,value)


    # Constantly read Data into Dataset, return the Dataset when the function is called

    def ReadDataSet(self):
        influxdb = Influxdb()
        influxdb.Query()
        #_thread.start_new_thread(self.DataSampling(self.data,1))
        #return self.data

    # store dataset in database
    def StoreDataArray(self):
        pass
