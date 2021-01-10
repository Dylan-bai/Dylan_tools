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
    filename = input('请输入文件名称：')
    readfile = open(filename, 'r')
    writename = open('D:/Users/LOG/经纬度计算.txt','a')
    while True:
        a = readfile.readline()
        if len(a) == 0:
            readfile.close()
            writename.close()
            break
        str1 = a.split(',')
        #转换坐标
        lon1, lat1, lon2, lat2 = map(float, [str1[11],str1[12],'121.3990865600','31.2624762100'])
        dis = haversine(lon1, lat1, lon2, lat2)
        writename.write(','.join(str1[7:14])+','+str(dis)+'\n')


if __name__ == "__main__":
    main()
    input("输入任意值结束")