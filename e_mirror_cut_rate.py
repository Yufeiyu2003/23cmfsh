from IntersectArea import *
from ColumnProjection import *
# from shapely.geometry import Polygon

from 求太阳各角度 import *
from 阳光向量 import *
from 求镜面顶点 import *
from 求镜面法向量 import *

import numpy as np


def e_mirror_cut_rate(phi,day,hour,mirror_center_point):
    '''
        返回 单面镜子 集热塔截断面积占比  截断效率
        
        维度phi 时间day hour  -- 太阳照射角度
        镜子中心坐标，  -- 镜子法向量&四角坐标
    '''

    # 计算镜子投影位置并旋转
    sun_vector = get_sun_vector(get_alpha_s(phi,day,hour),get_gamma_s(phi,day,hour))
    mirror_column = get_mirror_out_vector(mirror_center_point)
    mirror_points = get_mirror_point(mirror_center_point,get_mirror_normal_vector(mirror_center_point,sun_vector,mirror_column))
    x_points = ColumnProjection(mirror_column,mirror_points)
    
    # 坐标二维化
    points = x_points[:,[0,2]]

    # 集热塔面积
    tower = np.array([3.5,76],[3.5,84],[-3.5,84],[-3.5,76])
    
    # 计算截断面积
    cut_area,area = IntersectArea(tower,points)

    # 计算投射总面积
    cut_rate = area/cut_area

    return cut_rate