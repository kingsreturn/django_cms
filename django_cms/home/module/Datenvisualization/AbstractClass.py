from abc import abstractmethod,ABCMeta


class Visualization(metaclass=ABCMeta):
    def __init__(self):
        self.x_dataset=[]
        self.y_dataset=[]
