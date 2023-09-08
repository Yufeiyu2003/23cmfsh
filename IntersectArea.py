from shapely.geometry import Polygon

'''
输入两四边形在同一平面坐标系内的坐标
返回重叠面积
'''
def IntersectArea(tower,mirror):

    # data1 = [[1,1],[2,1],[2,3],[1,3]]

    # data2 = [[1,2],[1.5,1],[3,4],[2,4]]


    poly1 = Polygon(tower).convex_hull
    poly2 = Polygon(mirror).convex_hull

    if poly1.intersects(poly2):
        inter_area = poly1.intersection(poly2).area
    else:
        inter_area = 0

    return inter_area,poly2.area