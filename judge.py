import numpy as np
def judge(distances,i,judge_dis):
    #对于样本i，返回distance中距离i小于judge_dis且不等于0的样本
    #返回的是一个np.array
    return np.where((distances[i] < judge_dis) & (distances[i] != 0))[0] 