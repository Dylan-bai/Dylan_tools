import pandas as pd
raw_data = pd.read_csv('D:/Users/LOG/359464039842351.txt',index_col=None,names=[0,1],sep='~',engine='python')
print(raw_data)

raw_data1= pd.DataFrame(raw_data[0].str.extract('(\+RESP.*\$|\+BUFF.*\$)'))

raw_data1.to_csv('D:/Users/LOG/02.txt',index=None)