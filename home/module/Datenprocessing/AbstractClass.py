from abc import abstractmethod,ABCMeta


class Processing(metaclass=ABCMeta):
    def __init__(self,x_dataset,x_name,y_dataset,y_name):
        self.x_dataset=x_dataset
        self.x_name=x_name
        self.y_dataset=y_dataset
        self.y_name=y_name

    @abstractmethod
    def GenerateDataset(self):
        pass
