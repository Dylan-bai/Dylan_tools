file_reader = open('D:/Users/LOG/zhongyitong.txt','r')
# file_write = open('D:/Users/LOG/zhongyitong_12.txt','a')
file_write = open('D:/Users/LOG/zhongyitong_1.txt','a')
i=0
while True:
    line = file_reader.readline()
    if 0==len(line):
        file_reader.close()
        break
    line_split=line.split(',')
    # line_split[2] = '359464039242933'
    line_split[2] = ('00000000001000'[:(15-len(str(i)))]+str(i))
    line_split[4]= ('0000000000000001000'[:(20-len(str(i)))]+str(i))
    line_split[-4]=str(i)
    line_split[-1] = line_split[-1].replace('\n','$\n')
    print(line_split)
    file_write.write(','.join(line_split))
    i=i+1

# file_write = open('D:/Usersers/LOG/BLE_data.txt','a+')