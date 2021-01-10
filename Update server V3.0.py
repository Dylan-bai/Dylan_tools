import sys
import time
import socket
from threading import Thread
import re


class Logger(object):
    def __init__(self, log_path="default.log"):
        self.terminal = sys.stdout
        # self.log = open(log_path, "w", buffering=64)
        self.log = open(log_path, "ab", buffering=0)

    def print(self, *message):
        message = " ".join([str(it) for it in message])
        # self.terminal.write(str(message) + "\n")
        # self.log.write(str(message) + "\n")
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        self.terminal.write(str(otherStyleTime)+': '+str(message) + "\n")
        self.log.write(str(otherStyleTime).encode('utf-8')+b': '+str(message).encode('utf-8') + b"\n")

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def close(self):
        self.log.close()

#新建server用以监听
'''
serverd 
1、建立socket链接
2、监听端口
3、处理升级过程逻辑
'''
class Server(object):

    def __init__(self,port,filename):
        '''初始化server，实列化升级终端，做好升级准备工作'''
        self.gserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gserver.bind(('',port))
        self.gserver.listen(512)
        self.dict1 = {}
        self.server_pool={}

        r_file = open(filename, 'r')
        while True:
            imei = r_file.readline().strip('\n')
            if 0 == len(imei):
                r_file.close()
                break
            self.dict1[imei] = Device_que(imei)
        log.print('Ready.....')

    def listion(self):
        '''创建多线程处理client'''
        while True:
            new_socket,addr = self.gserver.accept()
            t1 = Thread(target=self.processing,args=(new_socket,addr))
            t1.setDaemon(True)
            t1.start()

    def processing(self,new_socket,addr):
        '''升级处理逻辑'''
        while True:
            raw_data = new_socket.recv(2048)
            # print(str(addr)+raw_data.decode('utf-8'))
            # print(len(raw_data))
            if len(raw_data)==0:
                new_socket.close
                del server.server_pool[new_socket]
                break
            log.print(str(addr)+'\t'+raw_data.decode('utf-8'))
            # 增加服务器SACK回复，心跳包必须要按照下面的格式回复
            self.Server_Sack(new_socket,raw_data)
            #升级过程处理
            self.UpdateProcess(new_socket,raw_data,addr)


    def Server_Sack(self,new_socket,raw_data):
        '''服务器确认使能'''
        data_split = raw_data.decode('utf-8').split(',')
        # 增加服务器SACK回复，心跳包必须要按照下面的格式回复
        if data_split[0][-5:] == 'GTHBD':
            new_socket.sendall('+SACK:GTHBD,,'.encode('utf-8') + raw_data[-5:])
        else:
            new_socket.sendall('+SACK:'.encode('utf-8') + raw_data[-5:])

    def UpdateProcess(self,new_socket,raw_data,addr):
        # 根据原始报文中的IMEI号查找启动server创建的实列
        device = self.dict1[re.findall('\d{15}', raw_data.decode('utf-8'))[0]]
        # 记录设备IMEI号和链接的关系，方便发指令
        self.server_pool [new_socket] = [addr,re.findall('\d{15}', raw_data.decode('utf-8'))[0]]

        raw_data_split = raw_data.decode('utf-8').split(',')
        # 调试定时
        # print('device.timesleep is :'+str(device.timesleep))
        # print('device.sendmessage is :'+str(device.sendmessage))
        if raw_data_split[0][-5:] == 'GTUPD' or device.sendmessage == 1:
            device.sendmessage = 1
        if device.sendmessage != 1:
            new_socket.sendall(device.updmessage.encode('utf-8'))
            device.sendmessage = 1
            log.print('=>' + '\t' + re.findall('\d{15}', raw_data.decode('utf-8'))[0] + '\t' + device.updmessage)
        if raw_data_split[0][-5:] == 'GTUPD':
            if raw_data_split[4] == '301':
                new_socket.sendall(device.srimessage.encode('utf-8'))
                log.print('=>' + '\t' + re.findall('\d{15}', raw_data.decode('utf-8'))[
                    0] + '\t' + device.srimessage)
            elif raw_data_split[4] in ['101', '102', '103', '202', '302', '303']:
                if device.updatemax < 3 and device.timesleep == 0:
                    # 睡眠120s乘以计数device.updatemax
                    th = Thread(target=device.timedelay)
                    th.start()
                else:
                    log.print('=>   failed  ' + re.findall('\d{15}', raw_data.decode('utf-8'))[0])


class Device_que(object):

    '''设备实列化,实列化'''
    def __init__(self,IMEI):
        self.imei = IMEI
        self.sendmessage = 0
        self.upd10x = None
        self.upd20x = None
        self.upd30x = None
        self.updatemax = 0
        self.updmessage = updmessage
        self.srimessage = srimessage
        self.timesleep = 0

    def timedelay(self):
        '''增加倒计时，如果升级失败可以实现多次升级'''
        self.timesleep = 1
        time.sleep(int(120 * (self.updatemax + 1)))
        self.updatemax += 1
        self.sendmessage = 0
        self.timesleep = 0

def hand_message():
    while True:
        try:

            input_message = input('pls input port and message：' + '\n').split('||')
            # 判断是否查询列表，如果是'ls'则返回设备链接列表
            if input_message[0] != 'ls':
                for item, value in server.server_pool.items():
                    if value[0][1] == int(input_message[0]):
                        item.sendall(input_message[1].encode('utf-8'))
                        log.print(value[1] + '\t' + input_message[1])
            else:
                log.print('Now,Devices list:')
                log.print('*' * 50)
                for item, value in server.server_pool.items():
                    log.print(str(value))
                log.print("*" * 50)
        except:
            log.print(KeyError)


if __name__ == '__main__':
    global log
    log = Logger()
    port = input('Pls input server port:')
    updmessage = input('Pls input AT+GTUPD command:')
    srimessage = input('Pls input AT+GTSRI command:')
    try:
        server = Server(int(port),'imei.txt')
        th_main = Thread(target=server.listion)
        th_main.start()
        hand_message()
    except:
        log.print(KeyError)
