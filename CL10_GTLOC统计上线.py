class CL10:
    '''CL10类，处理CL10信息'''
    def __init__(self,str):
        #print("我是CL10类")
       # write_file = open("hh3.txt","a")
        #write_file.write("我是新类\n")
        #write_file.close()
        #设备IMEI
        self.imei = str[3]
        #定位方式
        self.loc = str[6]
        #统计GPS定位的数量
        self.gps_num=0
        #统计WiFi定位的数量
        self.wifi_num = 0
        #统计基站定位的数量
        self.lbs_num = 0
        #统计报文总数
        self.num = 0
        #统计buff数量
        self.buff = 0
        #软件的版本
        self.version = str[2]
        #设备唤醒时间,几时几分
        self.time = str[1][1:12]
        #已上报条数
        self.report = str[-4]
        #剩余电量
        self.battery = str[-16]
        #上报时间点
        self.server_time = [0]*17


    def Loc_Mode(self,str):
        print("11111")
        print(str)
        print("11111")
        self.num += 1
        self.report = str[-4]
        self.battery = str[-16]
        if str[1][-10:-6] =='BUFF':
            self.buff += 1
        if str[7] == '01':
            self.gps_num += 1
        elif str[7] == '02':
            self.wifi_num += 1
        else:
            self.lbs_num += 1
    def Time(self,str):
       # print(str[1][1:12])
        #print(self.server_time)


        #输出每一天是否上报，其中服务器时间为self.time = str[1][1:12]
        if str[1][1:12] == '2019-12-07 ':
            #print('000000000')
            self.server_time [0] = 1
        elif str[1][1:12] == '2019-12-08 ':
            self.server_time[1] = 1
        elif str[1][1:12] == '2019-12-09 ':
            self.server_time[2] = 1
        elif str[1][1:12] == '2019-12-10 ':
            self.server_time[3] = 1
        elif str[1][1:12] == '2019-12-11 ':
            self.server_time[4] = 1
        elif str[1][1:12] == '2019-12-12 ':
            self.server_time[5] = 1
        elif str[1][1:12] == '2019-12-13 ':
            self.server_time[6] = 1
        elif str[1][1:12] == '2019-12-14 ':
            self.server_time[7] = 1
        elif str[1][1:12] == '2019-12-15 ':
            self.server_time[8] = 1
        elif str[1][1:12] == '2019-12-16 ':
            self.server_time[9] = 1
        elif str[1][1:12] == '2019-12-17 ':
            self.server_time[10] = 1
        elif str[1][1:12] == '2019-12-18 ':
            self.server_time[11] = 1
        elif str[1][1:12] == '2019-12-19 ':
            self.server_time[12] = 1
        elif str[1][1:12] == '2019-12-20 ':
            self.server_time[13] = 1
        elif str[1][1:12] == '2019-12-21 ':
            self.server_time[14] = 1
        elif str[1][1:12] == '2019-12-22 ':
            self.server_time[15] = 1
        elif str[1][1:12] == '2019-12-23 ':
            self.server_time[16] = 1

    def Miaoshu(self):
        return (self.imei, self.version,self.time, self.loc,self.num, self.gps_num, self.wifi_num, self.lbs_num,self.buff,
                self.report, self.battery)
    def re_time(self):
        return self.server_time
    def __str__(self):

        return "IMEI：%s\t\t定位方式:%s\t\tGPS定位数量：%d\t\tWiFi定位数量：%d\t\t基站定位数量：%d"%(self.imei,self.loc,self.gps_num,self.wifi_num,self.lbs_num)

def SF(file_name):
    '''对每一个IMEI.txt进行处理'''
    #file_name = input("请输入文件名称：")
    read_file = open(file_name,"r")
    one_line = read_file.readline()
    fenge = one_line.split(",")
    cl10 = CL10(fenge)
    read_file.close()
    read_file = open(file_name,"r")
    while True:
        one_line = read_file.readline()
        fenge = one_line.split(",")
        print('**1*')
        print(type(fenge))
        print(fenge)
        print(len(fenge))
        print('**1*')
        if len(one_line) == 0:
            #往1_data中写数据
            hui_write = open("1_data.txt", "a")
            #hui_write.write("IMEI\t版本\t时间\t定位方式\t总条数\tGPS定位方式\tWiFi\tLBS\tBUFF")
            res = []
            res = cl10.Miaoshu()
            for temp in  res:
                #print(a)
                hui_write.write(str(temp)+'\t')
            hui_write.write('\n')
            hui_write.close()

            #往2_data中写数据
            hui2_write = open("2_data.txt","a")
            #str(res[0])-> 表示IMEI号
            hui2_write.write(str(res[0])+'\t'+str(res[1]+'\t'))
            res2 = []
            res2 = cl10.re_time()
            for temp in res2:
                hui2_write.write(str(temp)+'\t')
            hui2_write.write('\n')
            hui2_write.close()
            break
        #m每一次都对类进行初始化，包括初始化上线时间
        cl10.Loc_Mode(fenge)
        cl10.Time(fenge)
def sort_imei(wenjianming):
    '''对IMEI号进行分类，并保存当对应IMEI.txt文档中，返回集合（IMEI)'''
    read_file = open(wenjianming,"r")
    jihe = set()
    while True:
        one_line = read_file.readline()

        if len(one_line) == 0:
            break
        fenge = []
        fenge = one_line.split(",")
        new_file = fenge[3] + ".txt"

        jihe.add(fenge[3])
        #print(jihe)
        write_file = open(new_file,"a")
        #print(one_line)
        write_file.write(one_line)
        write_file.close()
    read_file.close()
    return jihe

name = input("请输入文件名：")
#添加表头，详细介绍每台设备的上线情况
hui_write = open("1_data.txt","a")
hui_write.write("IMEI\t版本\t时间\t定位方式\t总条数\tGPS\tWiFi\tLBS\tBUFF\t已上报条数\t剩余电量\n")
hui_write.close()
#添加表头，分析每一天的上线情况
hui_write = open("2_data.txt","a")
hui_write.write("IMEI\n")
hui_write.close()
#这是一个集合
a = sort_imei(name)
for temp in a:
    new_name = temp + ".txt"
    print(new_name)
    #对每一个IMEI进行操作
    SF(new_name)





