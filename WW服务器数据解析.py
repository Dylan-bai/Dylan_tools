#1.判断是否为CL10设备，根据正则表达式patten='.+CL10.+'
#2.判断是否为GTLOC或者GTCID,如果是GTLOC执行函数GTLOC_AN否则执行GTCID_AN
#3.判断是否为严格意义一天一报
'''
实现功能，
1.分析每天上线数据
2.生成每台设备‘IMEI’.txt文件
3.
'''
class CL10():
    def __init__(self,str):
        '''imei,软件版本，定位优先级，定位方式，电量，CSQ用|隔开，唤醒时间，ICCID是否为0,buff数量，剩余电量，已上报条数'''
        self.imei =str[2]
        self.version = str[1]
        self.loc_mode = str[5]
        self.report_num = str[-4]
        self.num = 0
        self.buff = 0
        self.gps_num = 0
        self.wifi_num = 0
        self.lbs_num = 0
        self.battery = str[-16]
        self.CSQ = ''
        #如果有GTCID为空，则此位置0
        self.ICCID = 1
        #是否有GTCID报文
        self.gtcid = '否'
    def GTLOC_AN(self,str):
        self.num += 1
        self.report = str[-4]
        self.battery = str[-16]
        if str[1][-10:-6] == 'BUFF':
            self.buff += 1
        if str[6] == '01':
            self.gps_num += 1
        elif str[6] == '02':
            self.wifi_num += 1
        else:
            self.lbs_num += 1
        self.CSQ = self.CSQ+str[0][-10:-6]+str[-7]+'|'
    def GTCID_AN(self,str):
        self.gtcid = '是'
        if '' == str[4]:
            self.ICCID = 0
    def MIAOSHU(self):
        return (self.CSQ,self.ICCID)



def wanwei():


    pass




if __name__ == '__main__':
    readfilename = input('请输入文服务器件名称：')
    wanwei()