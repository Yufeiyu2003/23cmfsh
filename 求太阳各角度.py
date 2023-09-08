import numpy as np

#太阳赤纬角 delta
def get_sin_delta(Day):
    '''
    输入参数：Day，以春分为第0天的第Day天
    '''
    return np.sin(23.45*np.pi/180)*np.sin(2*np.pi*Day/365)

#太阳时角omega
def get_omega(hour):
    '''
    输入参数：hour，时间，以12:00为第0小时
    '''
    return np.pi*(hour-12)/12


#太阳高度角 alpha_s
def get_sin_alpha_s(phi,Day,hour):
    '''
    输入参数：phi，纬度
            Day，以春分为第0天的第Day天
            hour，时间，以12:00为第0小时
    '''
    sin_alpha_s = np.sin(phi)*get_sin_delta(Day) + np.cos(phi)*np.cos(get_omega(hour))*(1-get_sin_delta(Day)**2)**0.5
    return sin_alpha_s
def get_alpha_s(phi,Day,hour):
    '''
    输入参数：phi，纬度
            Day，以春分为第0天的第Day天
            hour，时间，以12:00为第0小时
    '''
    return np.arcsin(get_sin_alpha_s(phi,Day,hour))


#太阳方位角 gamma_s
def get_cos_gamma_s(phi,Day,hour):
    '''
    输入参数：phi，纬度
            Day，以春分为第0天的第Day天
            hour，时间，以12:00为第0小时
    '''
    cos_gamma_s = (get_sin_delta(Day)- get_sin_alpha_s(phi,Day,hour)*np.sin(phi))/(np.cos(get_alpha_s(phi,Day,hour)) *np.cos(phi))
    return cos_gamma_s

def get_gamma_s(phi,Day,hour):
    '''
    输入参数：phi，纬度
            Day，以春分为第0天的第Day天
            hour，时间
    '''
    if(hour<=12):
        return np.arccos(get_cos_gamma_s(phi,Day,hour))
    else:
        return 2*np.pi - np.arccos(get_cos_gamma_s(phi,Day,hour))

# if __name__ == "__main__":
#     import 阳光向量
#     import matplotlib.pyplot as plt
#     #测试
#     phi = -39.4*np.pi/180
#     Day = 90
#     sun_vector = np.array([0,0,0])
#     fig=plt.figure()
#     ax=fig.add_subplot(111,projection='3d')
#     for hour in range(6,19):
#         alpha_s = get_alpha_s(phi,Day,hour)
#         gamma_s = get_gamma_s(phi,Day,hour)
#         print("时间：",hour)
#         print("高度角：",alpha_s/np.pi*180,"方位角：",gamma_s/np.pi*180,"cos方位角：",get_cos_gamma_s(phi,Day,hour))
#         sun_vector = 阳光向量.get_sun_vector(alpha_s,gamma_s)
#         #画点
#         ax.scatter(sun_vector[0],sun_vector[1],sun_vector[2],c='r')

#     plt.show()


    
    

    
