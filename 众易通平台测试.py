import socket
import time

host = "gps06.cetgps3.com"
# host = "121.42.162.93"
host1 = "180.169.235.202"
port = 9696
port1 = 20439
#创建一个socket对象
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((host, port))
file_write = open('D:/Users/LOG/zhongyitong_test.txt','r')
while True:
    send_msg = file_write.readline().strip('\n')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client1.connect((host1, port1))
    if 0== len(send_msg):
        file_write.close()
        break
    client.send(send_msg.encode("utf-8"))
    client1.send(send_msg.encode("utf-8"))
    time.sleep(1)
    client.close()
    client1.close()
    # input("dddd")
# client.close()
# i=0
# print(time.time())
# while i<10:
#
#     send_msg = '+RESP:GTLOC,4D0800,359464039348326,CL10,89860446101970455735,2,01,1,0.0,270,52.1,116.724490,37.698903,' \
#                '20200318143924,0460,0000,5445,4A30,6,64,0,90,,,0,10,,0007,6,0,10,527,1500,20200318223924,020D$'
#     client.send(send_msg.encode("utf-8"))
#
#     i= i+10
#     time.sleep(2)
# client.close()
# print(time.time())