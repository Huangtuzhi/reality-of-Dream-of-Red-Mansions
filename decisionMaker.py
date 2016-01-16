#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm

class decisionMaker(object):
	def __init__(self):
		pass

	def train_and_predict_with_svm(self, train_data, train_data_label, predict_data):
		clf = svm.SVC()
		clf.fit(train_data, train_data_label)
		ret = clf.predict(predict_data)
		return ret

	def train_and_predict_with_regression(self, train_data, train_data_label, predict_data):
        # 应用Logistic回归进行预测
		LR = LogisticRegression()
		LR.fit(train_data, train_data_label)
		predict_labels = LR.predict(predict_data)
        # 0为不买的概率，1为买的概率
		predict_proba = LR.predict_proba(predict_data)[:, -1]
		return predict_labels, predict_proba

	def make_a_decision(self):
		trainset = np.load('trainset.npy')
		testset = np.load('testset.npy')

		train_data = trainset[:, 0:-1]   # 去除label后的特征数据
		train_data_label = trainset[:, -1]   # label
		test_data = testset[:, 0:-1]    # 去除label后的特征数据

		ret = self.train_and_predict_with_svm(train_data, train_data_label, test_data)
		print len(ret)
		print ret[0:80]
		print ret[80:120]


if __name__ == '__main__':
  	maker = decisionMaker()
  	maker.make_a_decision()