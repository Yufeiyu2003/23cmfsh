"""
输入  镜子到集热塔中心点的向量  镜子对应四个点坐标
输出平面化后的投射点坐标
"""
# 集热器中心点(column_center)  镜子中心点(mirror_center)  mirror_center:np.array,  column_center=np.array([0,0,76])
import numpy as np
from IntersectArea import *

TC=np.array([0,0,80])
TOWER = np.array([3.5,-4],[3.5,4],[-3.5,4],[-3.5,-4])

def ColumnProjection(mirror_to_column:np.array,mirror_points,mirror_center):
    # 通过向量求投射平面
    plane_vector = mirror_to_column.copy()
    plane_vector[2] = 0  # 求出投影平面法向量 非单位

    mod_v = np.sqrt(np.sum(plane_vector**2)) # 法向量的模

    # a = mirror_to_column[0]
    # b= mirror_to_column[1]
    # # plane = ax + by = 0

    ans = []
    for i in range(4):
        # 求距离

        # 直线距离
        distance_l = np.sqrt(np.sum(mirror_center**2 + TC**2))
        # 计算扩散半径
        ex_range = distance_l*0.0046251555
        # 垂直距离
        distance = np.abs(np.sum(plane_vector * mirror_points[i]))/mod_v
        multiple = distance/mod_v

        mirror_points[i] += mirror_to_column*multiple

    # 将坐标二维化  法向量和y轴重合
    
    # 夹角cos值
    cos_ = plane_vector[1]/mod_v
    # 夹角sin值
    sin_ = plane_vector[0]/mod_v
    R = np.array(
        [[cos_,-sin_,0],
        [sin_,cos_,0],
        [0,0,1]]
    )# 旋转矩阵
    points = mirror_points.dot(R)[:,[0,2]]
    points -= np.array([[0,TC[2]],[0,TC[2]]])
    
    # 计算放大倍率
    p1 = points[0]
    p2 = points[1]
    L = np.abs(p1[0]*p2[1]-p1[1]*p2[0])/np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    o_amplify_rate = (ex_range+L)/L
    o_points = points*o_amplify_rate
    i_amplify_rate = (L-ex_range)/L
    i_points = points*i_amplify_rate

    o_cut_area,o_area = IntersectArea(TOWER,o_points)
    m_cut_area,m_area = IntersectArea(TOWER,points)
    i_cut_area,i_area = IntersectArea(TOWER,i_points)

    # 被截断的面积(占自身面积)
    o_cut_area-=m_cut_area
    m_cut_area-=i_cut_area
    # 自身总面积
    o_area-=m_area
    m_area-=i_area

    total_energy = i_area + 0.75*m_area + 0.25*o_area
    residu_energy = i_cut_area + 0.75*m_cut_area + 0.25*o_cut_area

    energy_rate = residu_energy/total_energy

    return energy_rate