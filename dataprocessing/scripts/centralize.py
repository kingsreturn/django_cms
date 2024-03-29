#import numpy as np
from .Influxdb import Influxdb


class Centralized():
    def __init__(self,y_dataset,y_name):
        self.y_dataset=y_dataset
        self.y_name=y_name

    def Average(self, dataset):
        return sum(dataset) / len(dataset)
        #return np.average(dataset, axis=0)

    def GenerateProcessedData(self):
        average = sum(self.y_dataset) / len(self.y_dataset)#np.average(self.y_dataset, axis=0)
        for i in range(len(self.y_dataset)):
            self.y_dataset[i] -= average
        return self.y_dataset

    def StoreData(self):
        influx = Influxdb()
        influx.ConnnectDatabase()
        influx.WriteDataset('sensor', 'processed', self.y_name, self.y_dataset)


if __name__ == '__main__':
    dataset = Centralized([1, 2, 3, 4], 'time',[5, 6, 7, 8],'result')
    dataset.GenerateProcessedData()
    print(dataset.y_dataset)
    dataset.StoreData()
