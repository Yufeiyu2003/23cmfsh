import numpy as np
import 阳光向量 as sv
import 求太阳各角度 as sa
import 求镜面法向量 as mn
import 求镜面顶点 as mv
import 各效率 as ef
import e_mirror_rate as emr
import DNI
def get_sun(Day,Hour,phi):
    #太阳高度角
    alpha_s = sa.get_alpha_s(phi,Day,Hour)
    #太阳方位角
    gamma_s = sa.get_gamma_s(phi,Day,Hour)
    #太阳向量
    sun_vector = sv.get_sun_vector(alpha_s,gamma_s)

    return alpha_s,gamma_s,sun_vector


def get_efficiency( alpha_s,gamma_s,sun_vector,ID, mirror_point,L,W,data,dis_matrix,tower_shape_):
    '''
    alpha_s:太阳高度角
    gamma_s:太阳方位角
    sun_vector:太阳向量
    mirror_point:镜子中心点
    L:镜子长度
    W:镜子宽度
    tower_shape_:此时塔影
    '''
    

    ###############

    #镜面法向量
    mirror_normal_vector = mn.get_mirror_normal_vector(mirror_point,sun_vector,mn.get_mirror_out_vector(mirror_point))
    #镜面顶点
    mirror_vertex = mv.get_mirror_point(mirror_point,mirror_normal_vector,L,W)

    ###############
    eta_cos = ef.eta_cos(alpha_s,gamma_s,mirror_point)
    eta_at = ef.eta_at(mirror_point)
    eta_ref = ef.eta_ref()
    #截断效率,阴影效率:
    eta_trunc,eta_sb = emr.e_mirror_rate(ID,alpha_s,sun_vector,data,dis_matrix,tower_shape_)
    

    # #总效率
    # if(eta_cos<0):
    #     print("eta_cos<0")
    # if(eta_at<0):
    #     print("eta_at<0")
    # if(eta_ref<0):
    #     print("eta_ref<0")
    # if(eta_trunc<0):
    #     print("eta_trunc<0")
    eta = eta_cos * eta_at * eta_ref * eta_trunc * eta_sb

    all_eta = { "eta":eta, "eta_cos":eta_cos, "eta_at":eta_at,"eta_trunc":eta_trunc, "eta_sb":eta_sb}
    #print("第",ID,"个镜子效率:",all_eta)
    return all_eta


#d定日镜场输出热功率
def E_field(mirrors,dis_matrix,Day,Hour,phi,H):
    '''
    mirrors:镜子列表[底座x,底座y,安装高度z,尺寸长l,尺寸宽w]

    Day:天数,以春分为第0天
    Hour:时间,以12:00为第0小时
    phi:纬度
    H:海拔高度

    return:每个镜子的输出功率列表,总输出功率,单位镜面面积输出功率
    '''
    #环境数据
    alpha_s,gamma_s,sun_vector = get_sun(Day,Hour,phi)
    tower_shape_ = emr.tower_shape(sun_vector)

    DNI_value = DNI.get_DNI(alpha_s,H)
    # if(DNI_value<0):
    #     print("DNI<0")
    #每个镜子
    #mirror_point = mirrors[0:3]
    Ps =[]
    Areas=[]
    Ps_spre = []
    for id in range(len(mirrors)):
        mirror = mirrors[id]
        #效率
        efficiency = get_efficiency(alpha_s,gamma_s,sun_vector,id ,mirror[0:3],mirror[3],mirror[4],mirrors,dis_matrix,tower_shape_)
        #输出功率:DNI*镜面面积*效率
        Areas.append(mirror[3]*mirror[4])
        P = efficiency["eta"] * mirror[3] * mirror[4] * DNI_value
        Ps.append(P)
        Ps_spre.append(efficiency)
    
    P_sum = sum(Ps)
    Area_sum = sum(Areas)
    P_per_area = P_sum/Area_sum
    return Ps,P_sum,P_per_area,Ps_spre
    