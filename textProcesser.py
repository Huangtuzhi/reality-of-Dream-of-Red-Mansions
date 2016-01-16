#!/usr/bin/python
# -*- coding:utf-8 -*-

import string
import jieba
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")

class textProcesser(object):
	def __init__(self):
		pass

	# 将书分为章节
	def divide_into_chapter(self):
		file_in = open('text/redmansions.txt', 'r')
		line = file_in.readline()
		chapter_cnt = 1
		chapter_text = ""

		while line:
			if '[(' in line:
				path_str = 'text/chapter-' + str(chapter_cnt)
				file_out = open(path_str, 'a')
				file_out.write(chapter_text)
				chapter_cnt += 1
				file_out.close()
				chapter_text = line
			else:
				chapter_text += line

			line = file_in.readline()

		file_in.close

	# 对一章分词
	def divide_into_words(self, document, docID):
		path_str = 'text/chapter-words-' + str(docID)
		file_out = open(path_str,'a')

		line = document.readline()
		while(line):
			seg_list = jieba.cut(line, cut_all=False)
			words = " ".join(seg_list)
			file_out.write(words)
			line = document.readline()
		file_out.close()

	# 对所有章节分词
	def perform_segmentation(self):
		for loop in range(1, 121):
			path_str = 'text/chapter-' + str(loop)
			file_in = open(path_str, 'r')
			self.divide_into_words(file_in, loop)

	# 将每个文档去除标点后，再进行词频统计
	def count_words(self, document, docID):
		result_dict = {}
		delset = string.punctuation

		line = str(document)
		line = line.translate(None, delset) #去除英文标点
		line = "".join(line.split('\n')) # 去除回车
		line = self.sub_replace(line) #去除中文标点
		word_array = []
		words = line.split()
		for word in words:
			if not result_dict.has_key(word):
				result_dict[word] = 1
			else:
				result_dict[word] += 1

		path_str = 'text/chapter-wordcount-' + str(docID)
		file_out = open(path_str,'a')

		# 排序后写入文本
		sorted_result = sorted(result_dict.iteritems(), key=lambda d:d[1], reverse = True)
		for one in sorted_result:
			line = "".join(one[0] + '\t' + str(one[1]) + '\n')
			file_out.write(line)
		file_out.close()

	# 对所有文档进行分词
	def perform_wordcount(self):
		for loop in range(1, 121):
			path_str = 'text/chapter-words-' + str(loop)
			file_in = open(path_str, 'r')
			line = file_in.readline()
			document = ""
			while line:
				document += line
				line = file_in.readline()
			self.count_words(document, loop)
			file_in.close()

	def sub_replace(self, line):
		regex = re.compile(ur"[^\u4e00-\u9fa5a-zA-Z0-9\s]")
		return regex.sub('', line.decode('utf-8'))

if __name__ == '__main__':
	processer = textProcesser()
	processer.divide_into_chapter()
	processer.perform_segmentation()
	processer.perform_wordcount()