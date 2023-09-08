import numpy as np
#输入镜面中心,阳光向量
#输出镜面中心的镜面向量(即中间向量)

#加热塔中心坐标
HEATING_TOWER_CENTER=np.array([0,0,80])

def get_mirror_out_vector( mirror_center_point):
    out=HEATING_TOWER_CENTER-mirror_center_point
    return out/ np.linalg.norm(out)

def get_mirror_normal_vector( mirror_center_point, sun_vector):
    #异常处理
    if(len(mirror_center_point)!=3 or len(sun_vector)!=3):
        print("输入参数错误")
        return None
    
    #入射光为阳光向量
    #出射光即为镜面中心与加热塔中心的连线
    #法向量为入射光与出射光方向的中间向量
    #出射光方向
    out_victor = get_mirror_out_vector(mirror_center_point)
    #法向量
    normal_vector = sun_vector + out_victor
    normal_vector = normal_vector/np.linalg.norm(normal_vector)
    if(normal_vector[2]<0):
        normal_vector = -normal_vector
    return normal_vector
