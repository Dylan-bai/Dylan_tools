import socket  # 导入 socket 模块
import time
from threading import Thread
import re

ADDRESS = ('', 20437)  # 绑定地址
g_socket_server = None  # 负责监听的socket
g_conn_pool = []  # 连接池

class Device_que(object):
    def __init__(self,IMEI):
        self.imei = IMEI
        self.sendmessage = 0
        self.upd10x = None
        self.upd20x = None
        self.upd30x = None
        self.updatemax = 0


def start():
    name = input('请输入待升级的IMEI文件名：')
    r_file = open(name,'r')
    while True:
        oneline = r_file.readline().strip('\n')
        if 0==len(oneline):
            r_file.close()
            break
        # de = 'de'+oneline
        #创建IMEI对象
        # de = Device_que(oneline)
        dict1[oneline]= Device_que(oneline)
        # print(dict1)

    # print(device)

def initserver():
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(512)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print('服务器已启动，等待客户连接')

def listion():
    client,_ = g_socket_server.accept()
    g_conn_pool.append(client)
    # print(client)
    # print('*'*88)
    # print(_)
    th = Thread(target=message_handle,args=(client,_,))
    #设置守护线程
    th.setDaemon(True)
    th.start()

def message_handle(client,_):
    while True:
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        raw = client.recv(2048)
        if len(raw) == 0:
            client.close()
            # 删除连接
            g_conn_pool.remove(client)
            print(str(_)+"客户端下线了。")
            print(device.imei+"设备下线了。")
            break
        raw_split =  raw.decode(encoding='utf8').split(',')
        with open("1.txt", "a", encoding="UTF-8") as f:
            f.write(str(otherStyleTime)+str(_)+'收到的原始log：'+raw.decode(encoding='utf8')+'\n')
        # print(raw_split[2]) #IMEI
        # print(raw_split[4]) #升级过程
        #增加判断，如果检测有ACK回复或者'100'，则不发送升级指令
        # device = 'de'+raw_split[2]
        # if raw_split[2] not in dict1.keys():
        #     print('break')
        #     break
        # device = dict1[raw_split[2]]
        device = dict1[re.findall('86\d{13}',str(raw.decode(encoding='utf8')))[0]]
        # device = Device_que(raw_split[2])   #调试使用
        # print(raw_split[0][-5:])
        # print(device.sendmessage)
        if raw_split[0][-5:] == 'GTUPD'or device.sendmessage==1:
            device.sendmessage = 1
            # print('upd shoudo')

        if device.sendmessage != 1:
            client.sendall('AT+GTUPD=zk600,0,,10,0,http://iot.spin.pm:8080/ninebot/firmware/iot/R05A03V02.enc,,0,0,,,,FFFF$'.encode(encoding='utf8'))
            device.sendmessage=1
            with open("1.txt", "a", encoding="UTF-8") as f:
                f.write(str(otherStyleTime)+str(_) +'向'+ re.findall('86\d{13}',str(raw.decode(encoding='utf8')))[0]
                        +'发送的指令：' + 'AT+GTUPD=zk600,0,,10,0,http://iot.spin.pm:8080/ninebot/firmware/iot/R05A03V02.enc,,0,0,,,,FFFF$' + '\n')

        # if raw_split[4]=='301' and raw_split[0][-5:] == 'GTUPD':
        #     print('*'*12)
        #     time.sleep(3)
        #     client.sendall('AT+GTBSI=zk600,iot.spin.pm,8383,FFFF$'.encode(encoding='utf8'))
        #     with open("1.txt", "a", encoding="UTF-8") as f:
        #         f.write(str(otherStyleTime)+str(_) + re.findall('86\d{13}',str(raw.decode(encoding='utf8')))[0]+
        #                 '升级成功,并发送的指令：' + 'AT+GTBSI=zk600,iot.spin.pm,8383,FFFF$' + '\n')
        #根据升级协议，分别打印出对应log到指令文件中
        if raw_split[0][-5:] == 'GTUPD':
            if raw_split[4]=='301':
                time.sleep(3)
                client.sendall('AT+GTBSI=zk600,iot.spin.pm,8383,FFFF$'.encode(encoding='utf8'))
                with open("1.txt", "a", encoding="UTF-8") as f:
                    f.write(str(otherStyleTime)+str(_) + re.findall('86\d{13}',str(raw.decode(encoding='utf8')))[0]+
                                '升级成功,并发送的指令：' + 'AT+GTBSI=zk600,iot.spin.pm,8383,FFFF$' + '\n')
                with open("log2.txt", "a", encoding="UTF-8") as f:
                    f.write(str(otherStyleTime)+'\t'+re.findall('86\d{13}',str(raw.decode(encoding='utf8')))[0]+'\t'+
                            'Update successed：'+'\t'+raw_split[4]+ '\n')
                with open("E:/Server/FotaToolV0.06/FotaToolV0.06 8594/project/Server/deltabin/log2.txt", "a", encoding="UTF-8") as f:
                    f.write(str(otherStyleTime)+'\t'+
                            'Update successed:'+'\t'+ re.findall('86\d{13}',str(raw.decode(encoding='utf8')))[0]+'\n')

            elif raw_split[4] in ['101','102','103','202','302','303']:
                # print('upadtemax'+str(device.updatemax) )
                # print(device.updatemax < 2)
                #控制最多下发升级指令的次数，如果发现升级失败，尝试多发一次升级指令
                if device.updatemax < 3:
                    # 间隔2min之后再下发升级指令
                    print('-----:'+str(device.updatemax+1))
                    time.sleep(int(12*(device.updatemax+1)))
                    print('休眠时间是：'+str((13*(device.updatemax+1))))
                    device.sendmessage=0
                    device.updatemax+=1
                    # print('upadtemax'+str(device.updatemax))
                with open("log2.txt", "a", encoding="UTF-8") as f:
                    f.write(str(otherStyleTime)+'\t'+re.findall('86\d{13}',str(raw.decode(encoding='utf8')))[0]+'\t'+
                            'Upgrade failed：'+'\t'+raw_split[4]+ '\n')

            elif raw_split[4] in  ['100','200','201','300']:
                with open("log2.txt", "a", encoding="UTF-8") as f:
                    f.write(str(otherStyleTime)+'\t'+re.findall('86\d{13}',str(raw.decode(encoding='utf8')))[0]+'\t'+
                            'Upgrading：'+'\t'+raw_split[4]+ '\n')






        print(str(_)+'收到的原始log：'+raw.decode(encoding='utf8'))
        w_file.write(str(_)+'收到的原始log：'+raw.decode(encoding='utf8')+'\n')






if __name__ == '__main__':
    global dict1, w_file,j
    j=0
    dict1 ={}
    start()
    w_file = open('123.txt','w')
    w_file.write('1111')

    while True:
        # start()
        try:
            initserver()
            listion()
            # print(j)
            if j == len(dict1.keys()):
                w_file.close()
                exit()
        except:
            print(KeyError)

