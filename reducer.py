# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 21:11:15 2017

@author: Bokkin Wang
"""
#!/usr/bin/env python

import sys
def read_input(file):
    for line in file:
        yield line.rstrip()
    
input=read_input(sys.stdin)
mapperOut = [line.split('\t') for line in input]
cumVal1=0.0
cumVal2=0.0
cumSumSq1=0.0
cumSumSq2=0.0
cumN=0.0

for instance in mapperOut:
    nj = float(instance[0])  #第一字段是数据的个数
    cumN += nj               
    cumVal1 += nj*float(instance[1])  #第二字段是一个map输出loan均值，均值乘以数据个数就是数据总和
    cumSumSq1 += nj*float(instance[2])  #第三字段是一个map输出的loan平方和的均值，乘以元素个数就是所有元素的平方和
    cumVal2 += nj*float(instance[3])  #第四字段是也是一个map输出income均值，均值乘以数据个数就是数据总和
    cumSumSq2 += nj*float(instance[4])  #第五字段也是一个map输出的income平方和的均值，乘以元素个数就是所有元素的平方和

mean1 = cumVal1/cumN           #得到所有loan元素的均值
var1= (cumSumSq1/cumN-mean1*mean1)     #得到loan所有元素的方差
mean2 = cumVal2/cumN           #得到所有income元素的均值
var2= (cumSumSq2/cumN-mean2*mean2)     #得到所有income元素的方差
print "%s均值：%f\n%s均值：%f\n%s方差：%f\n%s方差：%f" % ("loan",mean1,"income",mean2,"loan",var1,"income",var2)




