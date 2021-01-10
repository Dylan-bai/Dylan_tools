import re

r_name = input('Pls input file name:')
patten = input('Pls input regular expression:')
# patten = '\d{1,2},\d{1,3}\.\d{1}.{3,11},\d{3}.\d{6},\d{2}.\d{6},\d{14}'
# print(patten)

w_name = 'log.txt'

r = open(r_name,'r')
w = open(w_name,'a')

while True:
    line = r.readline()
    if 0 == len(line):
        r.close()
        w.close()
        break
    result = re.findall(patten,line)
    # print(str(result))
    for i in result:
        w.write(i+'\n')