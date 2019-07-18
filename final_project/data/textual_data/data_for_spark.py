# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 17:19:02 2018

@author: Bokkin Wang
"""
import pickle as pkl
import tablib

#读取pkl有序向量，生成数据字典格式
x = open('C:/Users/Bokkin Wang/data/train_set.pkl', 'rb')
train_set = pkl.load(x,encoding='iso-8859-1')
x.close()

x = open('C:/Users/Bokkin Wang/data/train_tag.pkl', 'rb')
train_tag = pkl.load(x,encoding='iso-8859-1')
x.close()

x = open('C:/Users/Bokkin Wang/data/test_set.pkl', 'rb')
test_set = pkl.load(x,encoding='iso-8859-1')
x.close()

x = open('C:/Users/Bokkin Wang/data/test_tag.pkl', 'rb')
test_tag = pkl.load(x,encoding='iso-8859-1')
x.close()

#将序列中的每个元素转化为列表形式，并去除行间空格
train_set=[line.tolist() for line in train_set]
train_set=[line for line in train_set if line.__len__()!=1]

test_set=[line.tolist() for line in test_set]
test_set=[line for line in test_set if line.__len__()!=1]

#将标签放在训练集以及测试集的第一行中
train=[[train_tag[index]]+line for index,line in enumerate(train_set)]
test=[[test_tag[index]]+line for index,line in enumerate(test_set)]

#写出数据框文件，读出格式利用tsv格式，即利用\t进行分割
data = tablib.Dataset(*train)  
myfile = open('C:/Users/Bokkin Wang/data_rf/train.tsv', 'w')  
myfile.write(data.tsv)  
myfile.close()  

data = tablib.Dataset(*test)  
myfile = open('C:/Users/Bokkin Wang/data_rf/test.tsv', 'w')  
myfile.write(data.tsv)  
myfile.close()  
