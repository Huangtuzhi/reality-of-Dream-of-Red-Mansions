#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import numpy as np

reload(sys)
sys.setdefaultencoding("utf-8")

class modelBuilder(object):
	def __init__(self):
		pass

	def get_wordnum_of_chapter(self, DocID):
		path_str = 'text/chapter-' + str(DocID)
		file_in = open(path_str)

		text = ""
		for line in file_in:
			text += "".join(line.split('\n')) # 去除回车
		file_in.close

		num = len(text.decode("UTF-8"))
		return num

	# 每个文档提取特征向量
	def build_feature_vector(self, DocID, label):
		path_str = 'text/chapter-wordcount-' + str(DocID)
		
		# function_word_list = ['之', '其', '或', '亦', '方', '于', '即', '皆', '因', '仍', 
		# 					  '故', '尚', '呢', '了', '的', '着', '不', '乃', '呀', 
		# 					  '吗', '咧', '啊', '把', '让', '向', '往', '是', '在', '越', 
		# 					  '再', '更', '比', '很', '偏', '别', '好', '可', '便', '就',
		# 					  '但', '儿', # 42 个文言虚词
		# 					  '又', '也', # 高频副词
		# 					  '这', '那', '你', '我', '他' #高频代词
		# 					  '来', '去', '道', '笑'] #高频动词

		function_word_list = ['之', '其', '或', '亦', '方', '于', '即', '皆', '因', '仍', 
							  '故', '尚', '呢', '了', '的', '着', '一', '不', '乃', '呀', 
							  '吗', '咧', '啊', '把', '让', '向', '往', '是', '在', '越', 
							  '再', '更', '比', '很', '偏', '别', '好', '可', '便', '就',
							  '但', '儿',                 # 42 个文言虚词
							  '又', '也', '都', '要',      # 高频副词
							  '这', '那', '你', '我', '他' # 高频代词
							  '来', '去', '道', '笑', '说' #高频动词
							  ] 
		feature_vector_list = []

		for function_word in function_word_list:
			
			find_flag = 0
			file_in = open(path_str) #每次打开移动 cursor 到头部
			line = file_in.readline()
			while line:
				words = line[:-1].split('\t')
				if words[0] == function_word:
					total_words = self.get_wordnum_of_chapter(DocID)
					rate = float(words[1]) / total_words * 1000
					rate = float("%.6f" % rate)# 指定位数
					feature_vector_list.append(rate)
					# print words[0] + ' : ' + line

					file_in.close()
					find_flag = 1
					break
				line = file_in.readline()

			# 未找到词时向量为 0
			if not find_flag:
				feature_vector_list.append(0) 

		feature_vector_list.append(label)
		return feature_vector_list

	def make_positive_trainset(self):
		positive_trainset_list = []
		for loop in range(20, 30):
			feature = self.build_feature_vector(loop, 1) #label 为 1 表示正例
			positive_trainset_list.append(feature)
		# print positive_trainset_list
		np.save('pos_trainset.npy', positive_trainset_list)

	def make_negative_trainset(self):
		negative_trainset_list = []
		for loop in range(110, 120):
			feature = self.build_feature_vector(loop, 2) #label 为 0 表示负例
			negative_trainset_list.append(feature)
		# print negative_trainset_list
		np.save('neg_trainset.npy', negative_trainset_list)

	def make_trainset(self):
		feature_pos = np.load('pos_trainset.npy')
		feature_neg = np.load('neg_trainset.npy')
		trainset = np.vstack((feature_pos, feature_neg))
		np.save('trainset.npy', trainset)

	def make_testset(self):
		testset_list = []
		for loop in range(1, 121):
			feature = self.build_feature_vector(loop, 0) #无需 label，暂设为 0
			testset_list.append(feature)
		# print testset_list
		np.save('testset.npy', testset_list)


if __name__ == '__main__':
  	builder = modelBuilder()
	# print builder.build_feature_vector(1)

	builder.make_positive_trainset() 	
	builder.make_negative_trainset()

	builder.make_trainset()
	builder.make_testset()
