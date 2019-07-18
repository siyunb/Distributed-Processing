#!/bin/bash

PWD=$(cd $(dirname $0); pwd)
cd $PWD 1> /dev/null 2>&1

# hadoop client
STREAMING_DIR=/usr/lib/hadoop-current/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar 
HADOOP_INPUT_DIR=cufe_wangsiyu/lab2/linear_random.csv
HADOOP_OUTPUT_DIR=cufe_wangsiyu/lab2/result

echo $PWD
echo $HADOOP_INPUT_DIR
echo $HADOOP_OUTPUT_DIR

hadoop fs -rmr $HADOOP_OUTPUT_DIR

hadoop jar $STREAMING_DIR \
    -jobconf mapred.map.tasks=4 \
    -jobconf mapred.reduce.tasks=1 \
    -file  $PWD/matred.py $PWD/matmap.py \
    -output ${HADOOP_OUTPUT_DIR} \
    -input ${HADOOP_INPUT_DIR} \
    -mapper "matmap.py" \
    -reducer "matred.py" \

