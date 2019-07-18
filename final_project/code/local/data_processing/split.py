#-*-coding:utf-8-*-

import os
import pandas as pd
os.chdir("D:/bigdatahw/Case contest/data")
football = pd.read_excel('D:/bigdatahw/Case contest/data/football.xls')

for idx in list(range(football.shape[0])):
    if (len(str(football.iloc[idx,1]))>15):
        with open('D:/bigdatahw/Case contest/data/足球/'+str(idx)+'.txt','wb+') as f:
            f.write(football.iloc[idx,1].encode('utf8'))


