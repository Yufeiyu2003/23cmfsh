import numpy as np
#法向直接辐射辐照度

def get_DNI(alpha_s,H):
    '''
    alpha_s:太阳高度角
    H:海拔高度
    '''
    G_0=1.366 #太阳常数,单位kW/m^2
    a=0.4237 - 0.00821*(6 -H)**2
    b=0.5055 + 0.00595*(6.5 -H)**2
    c=0.2711 + 0.01858*(2.5 -H)**2
    DNI= G_0 *(a+b*np.exp(-c/np.sin(alpha_s)))
    return DNI
