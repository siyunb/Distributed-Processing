# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys

def read_input(file):
    for line in file:
        yield line.split(',')

sum11=0
sum12=0
sum21=0
sum22=0
num=0
num1=0
input = read_input(sys.stdin)
input1=[line[14].replace('"',' ') for line in input]
input2=[line[3].replace('"',' ') for line in input]
numInputs = len(input1)
for line in input1:
    num+=1
    if(num==1):
        name1=line
    else:
        sum11+=float(line)
        sum12+=float(line)*float(line)

for line in input2:
    num1+=1
    if(num1==1):
        name2=line
    else:
        sum21+=float(line)
        sum22+=float(line)*float(line)

print "%d\t%f\t%f\t%f\t%f" % (numInputs,sum11/numInputs, sum12/numInputs,sum21/numInputs,sum22/numInputs)
