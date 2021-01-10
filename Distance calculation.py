from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r


def main():
    # dis = haversine(118.611072,31.114733,118.620051,31.102072)
    filename = input("请输入统计里程文件名称：")
    readfile = open(filename, 'r')
    # lon1,lat1 = str(readfile.readline()).split(",")
    one_line = readfile.readline()
    lon1, lat1 = one_line.split(',')
    # print(lon1)
    # print(lat1)
    dis = 0.00000
    while True:
        a = readfile.readline()
        if len(a) == 0:
            readfile.close()
            break
        # print(a)
        lon2, lat2 = a.split(',')
        # 计算值
        lon1, lat1, lon2, lat2 = map(float, [lon1, lat1, lon2, lat2])
        dis = dis + haversine(lon1, lat1, lon2, lat2)
        lon1, lat1 = lon2, lat2
    print("总里程为：")
    print(dis)


if __name__ == "__main__":
    main()
    input("输入任意值结束")