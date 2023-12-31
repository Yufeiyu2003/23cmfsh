import numpy as np
import 定日镜光学效率 as eff
import test_multi
import multiprocessing

def draw_address(total_ring,同环间距,同环间距改变率,环间距,环间距改变率,high,Delta_high,H,W,是否均匀分散):
    """
    total_ring:总环数
    同环间距 弧度                                     0-1
    同环间距改变率:影响疏密改变速度(北密南疏) [a,b] 其中a>=0 b>=0
    环间距
    环间距改变率： 越往外间距越大   [a,b] 其中a>=0 b>=0
    high: 初始高度
    Delta_high: 高度改变速率   [a,b] 其中a>=0 b>=0
    H:长
    W:宽

    初始环半径100

    输出  x y z H W
    """

    data = []
    同环间距改变率[0]/=10000
    同环间距改变率[1]/=100
    Delta_high[0]/=1000
    Delta_high[1]/=10
    

    # 定环半径    
    if 环间距>(W+5):
        ring_space = 环间距
    else:
        ring_space = W+5


    def ring_R(n):
        # 初始环 环0  第n环半径
        return 环间距改变率[0]*n**2 + (1+环间距改变率[1])*(ring_space)*n + 100
    
    # 高度
    def hight(n):

        temp = -Delta_high[0]*n**2 - Delta_high[1]*n + high
        if temp < H/2:   # 不触及地面
            return H/2
        else:
            return temp

    
    

    for n in range(total_ring):
        R = ring_R(n)
        min_space = 2*np.arcsin(((5+W)/2)/R)
        同环间距 = 2*np.arcsin(((同环间距)/2)/R)
        if 同环间距>(min_space):
            space = 同环间距
        else:
            space = min_space

        # 同环间距
        def space_each(n):
            return 同环间距改变率[0]*n**2+ 同环间距改变率[1]*n+space
        
        max_num = np.pi//space
        # print(min_space)
        # print(max_num)

        if 是否均匀分散:
            per = (np.pi*2)//space
            for i in range(int(per)):
                data.append([-R*np.sin(2*np.pi/per*i),R*np.cos(2*np.pi/per*i),hight(i),H,W])

        else:



            the_space = 0

            data.append([0,R,hight(0),H,W])    # 增加环初始点

            for i in range(1,int(max_num)+100):
                the_space += space_each(i)
                # print(i,space_each(i))
                #print(the_space)
                if the_space>np.pi-space_each(i+1)/2:
                    if the_space<np.pi:
                        data.append([0,-R,hight(i+1),H,W])
                    break
                else:
                    data.append([-R*np.sin(the_space),R*np.cos(the_space),hight(i),H,W])
                    data.append([R*np.sin(the_space),R*np.cos(the_space),hight(i),H,W])

    return np.array(data)




Max = [25,15,0.1,0.1,15,0.1,0.1,6,0.1,0.1,8,8]

min = [18,10,0,0,10,0,0,2,0,0,6,6]

phi=39.2*np.pi/180


def process_task(args):
    ps, tal, per = eff.E_field(args[2], args[3], args[0], args[1], phi, 3)
    return tal, per

def 优化目标(x):
    total_ring = x[0]   # 
    total_ring = int(total_ring)
    同环间距 = x[1]
    同环间距改变率 = x[2:4]
    环间距 = x[4]
    环间距改变率 = x[5:7]
    high = x[7]
    Delta_high = x[8:10]
    H = x[10]
    W = x[11]

    if H>W:
        temp = H
        H = W
        W = temp


    是否均匀分散 = 0
    ps_m = []
    tal_m = 0
    per_m = 0
 
    global mirrors
    global result_matrix
    mirrors = draw_address(total_ring,同环间距,同环间距改变率,环间距,环间距改变率,high,Delta_high,H,W,是否均匀分散)
    result_matrix = test_multi.range_result(mirrors[:, 0:2],8)

    




    

    task_list = [(0, 9,mirrors,result_matrix), (0, 12,mirrors,result_matrix), (0, 15,mirrors,result_matrix), (92, 9,mirrors,result_matrix), (92, 12,mirrors,result_matrix), (92, 15,mirrors,result_matrix), (275, 9,mirrors,result_matrix), (275, 12,mirrors,result_matrix), (275, 15,mirrors,result_matrix),(0, 9,mirrors,result_matrix), (0, 12,mirrors,result_matrix), (0, 15,mirrors,result_matrix)]

    # 创建一个进程池，可以根据需要调整进程数量
    pool = multiprocessing.Pool(processes=12)

    # 使用pool.map来并行执行任务，并获得结果
    results = pool.map(process_task, task_list)

    # 关闭进程池
    pool.close()
    pool.join()

    # 处理结果
    tal_m = 0
    per_m = 0
    for tal, per in results:
        tal_m += tal
        per_m += per

    # for day in [0,92,275]:
    #     for hour in [11,12,13]:
    #         ps,tal,per=eff.E_field(mirrors,result_matrix,day,hour,phi,3)
    #         tal_m += tal
    #         per_m += per
    #         if day == 0:
    #             tal_m += tal
    #             per_m += per

    if tal_m/12 >= 60000:
        return 60000+0.1*(tal_m/12) + per_m/12 *50000
    else:
        return tal_m/12
    



# if __name__ == "__main__":
#     # 定义要处理的任务列表
#     task_list = [(0, 9), (0, 12), (0, 15), (92, 9), (92, 12), (92, 15), (275, 9), (275, 12), (275, 15)]

#     # 创建一个进程池，可以根据需要调整进程数量
#     pool = multiprocessing.Pool(processes=8)

#     # 使用pool.map来并行执行任务，并获得结果
#     results = pool.map(process_task, task_list)

#     # 关闭进程池
#     pool.close()
#     pool.join()

#     # 处理结果
#     tal_m = 0
#     per_m = 0
#     for tal, per in results:
#         tal_m += tal
#         per_m += per

#     # 如果需要在day为0时再次添加tal和per，可以在这里添加

#     # 打印最终结果
#     print("tal_m:", tal_m)
#     print("per_m:", per_m)