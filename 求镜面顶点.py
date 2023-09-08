import numpy as np
import scipy.linalg as sl

import matplotlib.pyplot as plt
def get_mirror_point(mid_point,normal_vector,H,W,IS_PLOT = False):

    #异常处理
    if(len(mid_point)!=3 or len(normal_vector)!=3):
        print("输入参数错误")
        return None
    if(H<=0 or W<=0):
        print("输入参数错误")
        return None
    
    #法向量归一化
    normal_vector = normal_vector/np.linalg.norm(normal_vector)

    #mid_point为镜面中点
    #当法向量为[0,1,0]时，镜面为xoz平面,的四个顶点,称为原始顶点
    #原始顶点
    original_points = np.array([[W/2,0,H/2],[W/2,0,-H/2],[-W/2,0,-H/2],[-W/2,0,H/2]])
    original_normal_vector = np.array([0,1,0])

    #先绕z轴旋转,再绕旋转后的x轴旋转,保证镜面上下两边与地面平行
    #1.绕z轴旋转
    # 旋转角度
    theta = -np.arctan(normal_vector[1]/normal_vector[0])
    # 旋转矩阵
    Rz = np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])
    # 旋转后的法向量
    rotated_normal_vector = np.dot(Rz,original_normal_vector)
    # 旋转后的原始顶点
    rotated_points = np.dot(Rz,original_points.T).T

    #2.绕旋转后的x'轴旋转
    # 以旋转后的法向量为y
    # 旋转轴x'
    if(normal_vector[1]>0):
        x_axis = np.array([rotated_normal_vector[1],-rotated_normal_vector[0],0])
    else:
        x_axis = np.array([-rotated_normal_vector[1],rotated_normal_vector[0],0])
    theta = np.arctan(normal_vector[2]/(normal_vector[2]**2 + normal_vector[0]**2)**0.5)
    # 绕旋转轴旋转
    R = sl.expm(np.cross(np.eye(3),x_axis*theta))
    # 旋转后的法向量
    rotated_normal_vector = np.dot(R,rotated_normal_vector)
    # 旋转后的原始顶点
    rotated_points = np.dot(R,rotated_points.T).T

    #计算各顶点的坐标
    mirror_points = mid_point + rotated_points
    
    if(IS_PLOT== True) :
        # 画图
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        #画出原始顶点
        ax.scatter(original_points[:,0],original_points[:,1],original_points[:,2],c='r')
        #连线
        for i in range(4):
            ax.plot([original_points[i,0],original_points[(i+1)%4,0]],[original_points[i,1],original_points[(i+1)%4,1]],[original_points[i,2],original_points[(i+1)%4,2]],c='r')

        #画出旋转后的顶点
        ax.scatter(rotated_points[:,0],rotated_points[:,1],rotated_points[:,2],c='b')
        #连线
        for i in range(4):
            ax.plot([rotated_points[i,0],rotated_points[(i+1)%4,0]],[rotated_points[i,1],rotated_points[(i+1)%4,1]],[rotated_points[i,2],rotated_points[(i+1)%4,2]],c='b')


        #在线上绘制label
        for i in range(4):
            ax.text(original_points[i,0],original_points[i,1],original_points[i,2],str(i))
            ax.text(rotated_points[i,0],rotated_points[i,1],rotated_points[i,2],str(i))
        #画出原始法向
        ax.quiver(mid_point[0],mid_point[1],mid_point[2],original_normal_vector[0],original_normal_vector[1],original_normal_vector[2],length=1,color='r')
        #画出旋转后法向
        ax.quiver(mid_point[0],mid_point[1],mid_point[2],normal_vector[0],normal_vector[1],normal_vector[2],length=1,color='b')
        #等比例显示
        ax.set_aspect('equal')

        plt.show()


    return mirror_points

# if __name__ == "__main__":
#     #测试
#     get_mirror_point([0,0,0],[1,1,1],6,6,IS_PLOT=True)
#     get_mirror_point([0,0,0],[-1,-1,1],6,6,IS_PLOT=True)
#     get_mirror_point([0,0,0],[-1,1,1],6,6,IS_PLOT=True)
#     get_mirror_point([0,0,0],[1,-1,1],6,6,IS_PLOT=True)