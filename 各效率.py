import numpy as np
import scipy.linalg as sl
from 求镜面法向量 import HEATING_TOWER_CENTER
def eta_cos(alpha_s,gamma_s,mirror_point):
    #https://www.researching.cn/ArticlePdf/m00006/2010/30/9/2010-09-2652.pdf 式(6)
    #alpha_s:太阳高度角
    #gamma_s:太阳方位角
    #mirror_point:镜子中心点

    #集热塔中心点到镜子中心点的向量
    out_vector = mirror_point - HEATING_TOWER_CENTER
    #反射光线与竖直方向(Z轴方向)的夹角
    lambda_s = np.arccos(np.dot(out_vector,np.array([0,0,-1]))/np.linalg.norm(out_vector))
    #镜子在XOY平面上的投影与Y轴的夹角
    theta_H = np.arctan2(out_vector[0],out_vector[1])

    eta_cos = np.sqrt(2)/2 * ( np.sin(alpha_s) * np.cos(lambda_s) -np.cos(theta_H- gamma_s)*np.cos(alpha_s)*np.sin(lambda_s) +1 )**0.5
    return eta_cos

# if __name__ == "__main__":
#     print(eta_cos(0.00004*np.pi/180,178*np.pi/180 ,np.array([-1,-50,6])))