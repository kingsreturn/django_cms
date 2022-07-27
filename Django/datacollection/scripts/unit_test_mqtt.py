import numpy as np
import math
import itertools

x_data = np.linspace(0, 10, 100)
y_data =np.array([math.sin(x) for x in x_data])
above_limit = np.where(y_data > 0.9)[0]

def ranges(i):
    for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]


result = list(ranges(above_limit))
array = []
for x in result:
    for value in x:
        array.append(value/10.00)

print(array)
#for value in result:
    #for x in value:
        #value
    #print(value)
#print(result)
