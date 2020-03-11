import numpy as np
import math
import numpy as np
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
map = np.array([-1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1.,  1.,  1.,
        1.,  1.,  1.,  1.,  1.,  1., -1., -1.,  1.,  1.,  1.,  1.,  1.,
        1.,  1.,  1., -1., -1.,  1.,  1.,  1.,  1.,  4.,  1.,  1.,  1.,
       -1., -1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1., -1., -1.,  1.,
        1.,  1.,  1.,  1.,  1.,  1.,  1., -1., -1.,  1.,  1.,  1.,  1.,
        1.,  1.,  1.,  5., -1., -1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
        1., -1., -1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1., -1., -1.,
       -1., -1., -1., -1., -1., -1., -1., -1., -1.])
print(len(map))
normalizedMap = list()
for i in range(0,len(map), int(math.sqrt(len(map)))):
    normalizedMap.append(map[i:i+int(math.sqrt(len(map)))])
normalizedMap = normalizedMap
counter = 0
def counterSteps(  x, y):
    global counter
    global normalizedMap
    for i in [(1,1), (1,-1), (-1,-1),(-1,1)]:
        if(normalizedMap[x + i[0]][y + i[1]] == 1):
            normalizedMap[x + i[0]][y + i[1]] = -1
            counter +=1
            counterSteps(x + i[0] ,y + i[1] )
counterSteps(0,0)
print(counter)





