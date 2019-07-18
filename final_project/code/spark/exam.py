# -*- coding:utf-8 -*-
#导入相应的类
from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.evaluation import BinaryClassificationMetrics
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.classification import SVMWithSGD
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.tree import RandomForest
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession

sc = SparkContext(appName="WSY__homework")

#读取本地文件生成RDD,分别为单机处理过的训练集和测试集	
rawData=sc.textFile('file:///home/cufe1/cufe_wangsiyu/exam/data/train.tsv')
testData=sc.textFile('file:///home/cufe1/cufe_wangsiyu/exam/data/test.tsv')

#进行数据预处理，整理成labelpiont的spark可执行的形式
trimmed=rawData.map(lambda x:x.split('\t'))
label = trimmed.map(lambda x : x[-1])

data = trimmed.map(lambda x : (x[0],x[1:])).\
               map(lambda x:(int(x[0]), [float(yy) for yy in x[1]])).\
               map(lambda x:LabeledPoint(x[0],Vectors.dense(x[1])))

trimmed_test=testData.map(lambda x:x.split('\t'))
label_test = trimmed_test.map(lambda x : x[-1])

data_test = trimmed_test.map(lambda x : (x[0],x[1:])).\
               map(lambda x:(int(x[0]), [float(yy) for yy in x[1]])).\
               map(lambda x:LabeledPoint(x[0],Vectors.dense(x[1])))

#神经网络数据预处理
spark = SparkSession(sc)

#对数据进行缓存，同时统计训练数据样本的数目
data.cache()
data_test.cache()
numData = data.count()
numData_test = data_test.count()
print ('训练集数目：',numData)
print ('测试集数目：',numData_test)

#需要为朴素贝叶斯模型构建一份输入特征向量的数据,将负特征值设为0
nbdata = trimmed.map(lambda x : (x[0],x[1:])).\
                 map(lambda x:(int(x[0]), [float(yy) for yy in x[1]])).\
                 map(lambda x:(x[0], [0.0 if yy<0 else yy for yy in x[1]])).\
                 map(lambda x:LabeledPoint(x[0],Vectors.dense(x[1])))

nbdata_test = trimmed_test.map(lambda x : (x[0],x[1:])).\
                 map(lambda x:(int(x[0]), [float(yy) for yy in x[1]])).\
                 map(lambda x:(x[0], [0.0 if yy<0 else yy for yy in x[1]])).\
                 map(lambda x:LabeledPoint(x[0],Vectors.dense(x[1])))

#构建各种机器学习模型
numIteration = 10   #迭代次数
maxTreeDepth = 5    #树的深度

numClass = label.distinct().count()     #类别
print ('类别数：',numClass)

#训练逻辑回归、支持向量机、朴素贝叶斯、决策树模型、随机森林模型和神经网络模型
lrModel = LogisticRegressionWithSGD.train(data, numIteration)
svmModel = SVMWithSGD.train(data, numIteration)
nbModel = NaiveBayes.train(nbdata)
dtModel = DecisionTree.trainClassifier(data,numClass,{},impurity='entropy', maxDepth=maxTreeDepth)
rfModel = RandomForest.trainClassifier(data,numClasses=2,categoricalFeaturesInfo={},numTrees=300,featureSubsetStrategy="auto",impurity='gini', maxDepth=4, maxBins=32)
#mpModel = MultilayerPerceptronClassifier(maxIter=20,layers=[50,32,32 ,2], blockSize=128, seed=11)


print ('逻辑回归模型参数：',lrModel)
print ('支持向量机模型参数：',svmModel)
print ('朴素贝叶斯模型参数：',nbModel)
print ('决策树模型参数：',dtModel)
print ('随机森林模型参数：',rfModel)
#print ('神经网络模型参数：',mpModel)

#使用逻辑回归分类模型验证单个样本的分类状况
dataPoint = data_test.first()
prediction = lrModel.predict(dataPoint.features)
print ('预测的类别：',prediction)
print ('真实的类别：',int(dataPoint.label))

#验证支持向量机模型的准确性，验证前十个样本
predictions = svmModel.predict(data_test.map(lambda x : x.features))
print ('前十个样本的预测标签：',predictions.take(10))
print ('前十个样本的真实标签：',data_test.map(lambda x : x.label).map(lambda x: int(x)).take(10))

#逻辑回归模型模型的预测正确数目
lrTotalCorrect = data_test.map(lambda point : 1 if(lrModel.predict(point.features)==point.label) else 0).sum()
#支持向量机模型的预测正确数目
svmTotalCorrect = data_test.map(lambda point : 1 if(svmModel.predict(point.features)==point.label) else 0).sum()
#朴素贝叶斯模型的预测正确数目
nbTotalCorrect = nbdata_test.map(lambda point : 1 if (nbModel.predict(point.features) == point.label) else 0).sum()
#决策树模型的预测正确数目
predictLabel= dtModel.predict(data_test.map(lambda point: point.features)).collect()
trueLabel = data_test.map(lambda point: point.label).collect()
dtTotalCorrect = sum([1.0 if prediction == trueLabel[i] else 0.0 for i, prediction in enumerate(predictLabel)])
#随机森林模型的预测正确数目
predictions =rfModel.predict(data_test.map(lambda x: x.features)).collect() 
tureLabel = data_test.map(lambda lp: lp.label).collect()
rfTotalCorrect =  sum([1.0 if prediction == trueLabel[i] else 0.0 for i, prediction in enumerate(predictions)])
#神经网络模型的预测正确数目



#逻辑回归模型模型的预测正确率
lrAccuracy = lrTotalCorrect/(data_test.count()*1.0)
#支持向量机模型的预测正确率
svmAccuracy = svmTotalCorrect/(data_test.count()*1.0)
#朴素贝叶斯模型的预测正确率
nbAccuracy = nbTotalCorrect/(1.0*nbdata_test.count())
#决策树模型的预测正确率
dtAccuracy = dtTotalCorrect/(1.0*data_test.count())
#随机森林模型的预测正确率
rfAccuracy = rfTotalCorrect/(1.0*data_test.count())

print ('总共的样本数目: %s'%data_test.count())
print ('逻辑回归模型模型的预测正确率: %s'%lrAccuracy)
print ('支持向量机模型的预测正确率: %f'%svmAccuracy)
print ('朴素贝叶斯模型的预测正确率: %f'%nbAccuracy)
print ('决策树模型的预测正确率: %f'%dtAccuracy)
print ('随机森林模型的预测正确率: %f'%rfAccuracy)

# 模型评价
all_models_metrics = []
for model in [lrModel, svmModel]:
    scoresAndLabels = data_test.map(lambda point:(model.predict(point.features), point.label)).collect()
    scoresAndLabels = [[float(i),j] for i,j in scoresAndLabels]
    rdd_scoresAndLabels = sc.parallelize(scoresAndLabels)   #将数据转换为rdd
    metrics = BinaryClassificationMetrics(rdd_scoresAndLabels)
    all_models_metrics.append((model.__class__.__name__, metrics.areaUnderROC, metrics.areaUnderPR))
for modelName, AUC, PR in all_models_metrics:
    print ('%s的AUC是%f,PR是%f'%(modelName, AUC, PR))

scoresAndLabels = nbdata_test.map(lambda point:(nbModel.predict(point.features), point.label)).collect()
scoresAndLabels = [[float(i),j] for i,j in scoresAndLabels]

rdd_scoresAndLabels = sc.parallelize(scoresAndLabels)   #将数据转换为rdd
nb_metric = BinaryClassificationMetrics(rdd_scoresAndLabels)

print ('%s的AUC是%f,PR是%f'%(nbModel.__class__.__name__, nb_metric.areaUnderROC, nb_metric.areaUnderPR))

predictionLabels = dtModel.predict(data_test.map(lambda point: point.features)).collect()
trueLabels = data_test.map(lambda point: point.label).collect()
scoresAndLabels = [[prediction, trueLabel] for prediction,trueLabel in zip(predictionLabels, trueLabels)]
scoresAndLabels = [[float(i),j] for i,j in scoresAndLabels]
rdd_scoresAndLabels = sc.parallelize(scoresAndLabels)

dt_metric = BinaryClassificationMetrics(rdd_scoresAndLabels)
print ('%s的AUC是%f,PR是%f'%(dtModel.__class__.__name__, dt_metric.areaUnderROC, dt_metric.areaUnderPR))

predictionLabels = rfModel.predict(data_test.map(lambda point: point.features)).collect()
trueLabels = data_test.map(lambda point: point.label).collect()
scoresAndLabels = [[prediction, trueLabel] for prediction,trueLabel in zip(predictionLabels, trueLabels)]
scoresAndLabels = [[float(i),j] for i,j in scoresAndLabels]
rdd_scoresAndLabels = sc.parallelize(scoresAndLabels)

dt_metric = BinaryClassificationMetrics(rdd_scoresAndLabels)
print ('%s的AUC是%f,PR是%f'%(rfModel.__class__.__name__, dt_metric.areaUnderROC, dt_metric.areaUnderPR))



