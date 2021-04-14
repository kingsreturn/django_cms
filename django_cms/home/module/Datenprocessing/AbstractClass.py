from abc import abstractmethod,ABCMeta


class Processing(metaclass=ABCMeta):
    def __init__(self):
        self.x_dataset=[]
        self.y_dataset=[]
