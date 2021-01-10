import pandas as pd

def main():
    name = input('Pls input filename:')
    rawdata = pd.read_csv(name)
    d = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5]
    h = [-1000, -800, -500, -300, 400, 500, 1000]
    w_file = open('result.txt', 'a')
    for i in d:
        dis_shape = rawdata[rawdata['DIS'] > i].shape
        for j in h:
            if j < 0:
                alt_shape = rawdata[rawdata['Altitude'] < j].shape
                dis_alt = rawdata[(rawdata['DIS'] > i) & (rawdata['Altitude'] < j)].shape
                w_file.write(str(i) + '\t' + str(dis_shape[0]) + '\t' + str(j) + '\t' + str(alt_shape[0]) + '\t' + str(
                    dis_alt[0]) + '\n')
            else:
                alt_shape = rawdata[rawdata['Altitude'] > j].shape
                dis_alt = rawdata[(rawdata['DIS'] > i) & (rawdata['Altitude'] > j)].shape
                w_file.write(str(i) + '\t' + str(dis_shape[0]) + '\t' + str(j) + '\t' + str(alt_shape[0]) + '\t' + str(
                    dis_alt[0]) + '\n')


if __name__ == '__main__':
    main()