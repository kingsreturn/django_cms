import numpy as np

class Datenprocessing:
    def __init__(self,Dataset1:list,Dataset2:list):
        # parameter for Datenprozessing
        self.dataset1 = Dataset1
        self.dataset2 = Dataset2


    def CombineData(self):
        combined =[]
        combined.append(self.dataset1)
        combined.append(self.dataset2)
        return combined

    def Average(self,dataset):
        return np.average(dataset,axis =0)

if __name__ == '__main__':
    dataset = Datenprocessing([1,2,3,4],[5,6,7,8])
    print(dataset.Average(dataset.CombineData()))


