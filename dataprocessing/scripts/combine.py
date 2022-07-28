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
