from GroundProjection import *
from IntersectArea import *
from ColumnProjection import *
from shapely.geometry import Polygon

from 求太阳各角度 import *
from 阳光向量 import *
from 求镜面顶点 import *
from 求镜面法向量 import *

from judge import *  # 读取距离矩阵并分析

import numpy as np


TC=np.array([0,0,80])
# 集热塔大小
TOWER = np.array([[3.5,-4],[3.5,4],[-3.5,4],[-3.5,-4]])  # 集热器形状


def e_mirror_rate(ID,alpha_s,sun_vec,data,result):
    '''
        
        返回 单面镜子 集热塔截断面积占比  截断效率

        ID:镜子编号
        维度phi 时间day hour  -- 太阳照射角度
        镜子中心坐标，  -- 镜子法向量&四角坐标
    '''
    mirror_center_point = data[ID,0:3]
    # print(mirror_center_point)
    # 计算镜子投影位置并旋转
    sun_alpha = alpha_s
    sun_vector = sun_vec
    mirror_column = get_mirror_out_vector(mirror_center_point)
    mirror_points = get_mirror_point(mirror_center_point,get_mirror_normal_vector(mirror_center_point,sun_vector,mirror_column),data[ID,3],data[ID,4])


    #print(mirror_points)

    "截断效率"
    cut_rate = ColumnProjection(mirror_column,mirror_points.copy(),mirror_center_point)


    "阴影遮挡效率"
    shadow_area = 0
    #读取附近镜子
    max_range = (data[ID,2]+(data[ID,3]/2))/np.tan(sun_alpha)
    nearby = judge(result,ID,max_range)

    #获取自己的投影
    my_points = GroundProjection(mirror_points,sun_vector)
    poly1 = Polygon(my_points).convex_hull
    my_area = poly1.area
    # print(max_range)
    # print(my_points)
    for mirror_ID in nearby:
        # 假设附近镜子朝向和自己相差无几
        mirror = data[mirror_ID,0:3]
        m_mirror_points = get_mirror_point(mirror,get_mirror_normal_vector(mirror,sun_vector,get_mirror_out_vector(mirror)),data[mirror_ID,3],data[mirror_ID,4])
        o_points = GroundProjection(m_mirror_points.copy(),sun_vector)
        # print(o_points)
        #print(IntersectArea(poly1,o_points)[0])
        shadow_area += IntersectArea(poly1,o_points)[0]

    #print("shadow_area:",shadow_area,"my_area:",my_area)
    shadow_rate = 1-shadow_area/my_area

    return [cut_rate,shadow_rate]