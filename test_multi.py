import numpy as np
from multiprocessing import Pool

def distance(P1, P2):
    return np.sqrt(np.sum((P1 - P2) ** 2))

def compute_distance(i, j, data):
    if i < j:
        return distance(data[i, 0:1], data[j, 0:1])
    else:
        return 0

def range_result(data, pool_size=8):
    lendata = len(data)
    result = np.zeros((lendata, lendata))
    
    with Pool(pool_size) as pool:
        distances = pool.starmap(compute_distance, [(i, j, data) for i in range(lendata) for j in range(lendata)])
        
    # 把上三角矩阵result转化为对称矩阵
    for i in range(lendata):
        for j in range(lendata):
            if i > j:
                result[i][j] = distances[j * lendata + i]
                result[j][i] = distances[j * lendata + i]

    return result
# if __name__ == '__main__':
#     # 示例用法
#     data = np.array([[1, 2], [3, 4], [5, 6]])
#     result_matrix = range_result(data)
#     print(result_matrix)
