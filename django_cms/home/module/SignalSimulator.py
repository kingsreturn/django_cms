import random


class Simulator:
    def generateProcessingData(self):
        x_dataset = [0,1,2,3,4,5,6,7,8,9,10]
        y_dataset = []
        for i in range(0,11):
            y_dataset.append(random.randint(0,100))
        return x_dataset,y_dataset
