import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
#输入太阳高度角alpha_s和方位角gamma_s,计算三维阳光向量
def get_sun_vector(alpha_s,gamma_s):
    # #异常处理
    # if(alpha_s<0 or alpha_s>np.pi/2 or gamma_s<0 or gamma_s>2*np.pi):
    #     print("输入参数错误")
    #     return None
    #方位角gamma_s为0时，太阳向量指向Y轴正方向

    #太阳向量
    sun_vector = np.array([np.sin(gamma_s),np.cos(gamma_s),np.sin(alpha_s)])
    sun_vector = sun_vector/np.linalg.norm(sun_vector)
    return sun_vector

# if __name__ == "__main__":
#     #滑条输入太阳高度角alpha_s和方位角gamma_s,绘制三维阳光向量
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     alpha_s_0 = 0.0
#     gamma_s_0 = 0.0
#     sun_vector = get_sun_vector(alpha_s_0,gamma_s_0)
#     #绘制三维阳光向量
#     ax.quiver (0,0,0,sun_vector[0],sun_vector[1],sun_vector[2],length=1,normalize=True)
    
#     ax.set_title('Sun Vector')
#     #设置坐标轴范围
#     ax.set_xlim(-1,1)
#     ax.set_ylim(-1,1)
#     ax.set_zlim(-1,1)
#     #滑条
#     axcolor = 'lightgoldenrodyellow'
#     axalpha_s = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
#     axgamma_s = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
#     salpha_s = Slider(axalpha_s, 'alpha_s', 0.0, np.pi/2, valinit=alpha_s_0)
#     sgamma_s = Slider(axgamma_s, 'gamma_s', 0.0, 2*np.pi, valinit=gamma_s_0)

#     def update(val):
#         alpha_s = salpha_s.val
#         gamma_s = sgamma_s.val
#         sun_vector = get_sun_vector(alpha_s,gamma_s)
#         ax.clear()
#         ax.quiver (0,0,0,sun_vector[0],sun_vector[1],sun_vector[2],length=1,normalize=True)
#         ax.set_xlim(-1,1)
#         ax.set_ylim(-1,1)
#         ax.set_zlim(-1,1)
#         ax.set_title('Sun Vector')
#         fig.canvas.draw_idle()
#     salpha_s.on_changed(update)
#     sgamma_s.on_changed(update)
#     plt.show()
