'''
计算空间内任一点在光线向量 在xoy平面的投影坐标


'''

import numpy as np

def GroundProjection(point:np.array,vector:np.array):
    multiple = point[2]/vector[2]

    ans = point + multiple*vector

    ans[1] = 0

    return ans
    
    

