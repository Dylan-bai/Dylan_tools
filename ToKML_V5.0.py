import re
import pandas as pd
'''
1、先对报文进行排序
2、根据buff和速度自动判别使用不同点显示标记
'''
def Timestap(b):
    a = str(b)
    y, m, d = a[:4], a[4:6], a[6:8]
    h, min, s = a[8:10], a[10:12], a[12:14]
    datest = y + '/' + m + '/' + d + ' ' + h + ':' + min + ':' + s
    return datest

def ToCsv(name,w):
    #经纬度取值范围，-?\d{1,3}.\d{6},-?\d{1,2}.\d{6}
    patten = '[123456789],\d{1,3}\.\d{1}.{3,11},-?\d{1,3}.\d{6},-?\d{1,2}.\d{6},\d{14}'
    r = open(name,'r')
    while True:
        line = r.readline()
        if 0 == len(line):
            r.close()
            w.close()
            break
        result = re.findall(patten, line)
        line_split = line.split(',')
        if 'BUFF'in line:
            head = 'BUFF'
        else:head = 'RESP'
        # print(str(result))
        for i in result:
            w.write(head+','+i + '\n')
    rawdataname = name+'raw.txt'
    df = pd.read_csv(rawdataname,names=['Head','GNSS Accuracy','Speed','Azimuth','Altitude','Longitude','Latitude','UTC Time',])
    df.sort_values('UTC Time',inplace=True)
    df['Longitude'] = df['Longitude'].map(lambda x:'%.6f'%x)
    df['Latitude'] = df['Latitude'].map(lambda x:'%.6f'%x)
    df['UTC'] = df['UTC Time'].apply(Timestap)

    rawdatasortname = name + 'raw_data_sort.txt'
    df.to_csv(rawdatasortname,index = 0)
    return df

def ToKML(df,name):
    kmlname = name+'.kml'
    kml = open(kmlname,'a')
    tem = open('cfg.dll','r')
    lines = tem.read()
    kml.write(str(lines)+'\n')
    i = 1
    for row in df.iterrows():
        if row[1]['Head'] == 'RESP':
            if row[1]['Speed']>60:
                styleUrl = 'sn_grn-blank'
            else:
                styleUrl = 'sn_grn-blankbig'
        elif row[1]['Head'] == 'BUFF':
            if row[1]['Speed']>60:
                styleUrl = 'sn_pink-blank'
            else:
                styleUrl = 'sn_pink-blankbig'
        kml.write('\t<Placemark>\n')
        kml.write('\t\t<name>' + 'N.'+ str(i)+'</name>\n')
        kml.write('\t\t<styleUrl>#' + styleUrl + '</styleUrl>\n')
        kml.write('\t\t<description>#' + str(row[1]) + '</description>\n')
        kml.write('\t\t<Point>\n')
        kml.write('\t\t\t\t<coordinates>' + str(row[1]['Longitude'])  + ',' + str(row[1]['Latitude'])  + '</coordinates>\n')
        kml.write('\t\t</Point>\n')
        kml.write('\t</Placemark>\n')
        i+=1
    kml.write('\t<Placemark>\n')
    kml.write('\t\t<styleUrl>#yellowLineGreenPoly</styleUrl>\n')
    kml.write('\t\t<LineString>\n')
    kml.write('\t\t\t<coordinates>\n')
    for row in df.iterrows():
        kml.write(str(row[1]['Longitude'])  + ',' + str(row[1]['Latitude'])+'\n')
    kml.write('</coordinates>\n')
    kml.write('\t\t</LineString>\n')
    kml.write('\t</Placemark>\n')
    kml.write('</Document>\n')
    kml.write('</kml>')
    kml.close()
    tem.close()







if __name__=='__main__':
    read_name = input('Pls input file name:')
    rawdataname = read_name + 'raw.txt'
    write_name = open(rawdataname,'a')
    a = ToCsv(read_name,write_name)
    ToKML(a,read_name)
