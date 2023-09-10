import numpy as np

def draw_address(total_ring,同环间距,同环间距改变率,环间距,环间距改变率,high,Delta_high,H,W,是否均匀分散):
    """
    total_ring:总环数
    同环间距 弧度
    同环间距改变率:影响疏密改变速度(北密南疏) [a,b] 其中a>=0 b>=1
    环间距
    环间距改变率： 越往外间距越大   [a,b] 其中a>=0 b>=1
    high: 初始高度
    Delta_high: 高度改变速率   [a,b] 其中a>=0 b>=0
    H:长
    W:宽

    初始环半径100

    输出  x y z H W
    """

    total_mirror = 0
    data = []

    # 定环半径    
    if 环间距>(W+5):
        ring_space = 环间距
    else:
        ring_space = W+5


    def ring_R(n):
        # 初始环 环0  第n环半径
        return 环间距改变率[0]*n**2 + 环间距改变率[1]*(ring_space)*n + 100
    
    # 高度
    def hight(n):
        return Delta_high[0]*n**2 + Delta_high[1]*n + high


    


    for n in range(total_ring):
        R = ring_R(n)
        min_space = 2*np.arcsin(((5+W)/2)/R)
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

    return data