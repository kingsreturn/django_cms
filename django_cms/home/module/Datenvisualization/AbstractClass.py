from abc import abstractmethod,ABCMeta


class Visualization(metaclass=ABCMeta):
    def __init__(self):
        self.x_dataset=[]
        self.x_name=''
        self.y_dataset=[]
        self.y_name=''

    @abstractmethod
    def plot(self):
        pass
