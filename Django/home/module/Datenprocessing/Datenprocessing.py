import numpy as np
from .AbstractClass import Processing


class Datenprocessing(Processing):
    def __init__(self, Dataset1: list, Dataset2: list):
        # parameter for Datenprozessing
        self.dataset1 = Dataset1
        self.dataset2 = Dataset2

    def CombineData(self):
        combined = []
        combined.append(self.dataset1)
        combined.append(self.dataset2)
        return combined

    def Average(self, dataset):
        return np.average(dataset, axis=0)

    def GenerateDataset(self):
        pass

class Centralized(Processing):
    def Average(self, dataset):
        return np.average(dataset, axis=0)

    def GenerateDataset(self):
        average = np.average(self.y_dataset, axis=0)
        print(average)
        for i in range(len(self.y_dataset)):
            self.y_dataset[i] -= average


if __name__ == '__main__':
    dataset = Centralized([1, 2, 3, 4], 'time',[5, 6, 7, 8],'result')
    dataset.GenerateDataset()
    print(dataset.y_dataset)
