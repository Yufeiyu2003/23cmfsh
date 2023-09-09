'''
计算空间内任一点在光线向量 在xoy平面的投影坐标


'''

import numpy as np

def GroundProjection(points:np.array,vector:np.array):
    for point in points:
        multiple = point[2]/vector[2]
        point += multiple*vector
    
    return points[:,0:2]
    
    

# np.tile(vector,[4,1])