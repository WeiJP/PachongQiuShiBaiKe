# -*- coding:utf-8 -*-
# 2017-03-10 15:43
# auther:wjp
# 糗事百科

import urllib
import urllib2
import re
from subprocess import call

class QiuShiBaiKe(object):
	"""抓取糗事百科的数据"""
	def __init__(self):
		#页码索引
		self.pageIndex = 1
		#容器，每个元素是一整页的段子
		self.storyPages = []
		#程序是否继续运行的标识
		self.stop = True
		#是否朗读
		self.voice = False

	# 抓取某一页全部的数据
	def getData(self, pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0)'
			headers = { 'User-Agent' : user_agent }
			request = urllib2.Request(url, headers = headers)
			response = urllib2.urlopen(request)
			return response.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print '--------------------------'
                print u"连接糗事百科失败,错误原因：\n",e.reason
                print '--------------------------'
                return None

    #解析整页数据并返回一个数组
	def analyticalData(self, pageIndex):
		pageData = self.getData(self.pageIndex)
	    	if not pageData:
	    		print '--------------------------'
	    		print "数据抓取失败..."
	    		print '--------------------------'
	    		return None

	    	pattern = re.compile('<div.*?author clearfix">.*?<a href.*?<h2>(.*?)</h2>.*?<div.*?content">.*?<span>(.*?)</span>.*?</a>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
	    	items = re.findall(pattern, pageData)
	    	stories = []
	    	for item in items:
				haveImg = re.search("img", item[2])
				if not haveImg:
					showString = item[1].replace('<br/>', '\n')
					stories.append([item[0].strip(), showString.strip(), item[3].strip()])
	        return stories

	#开始展示数据，并根据设置是否朗读
	def showStory(self):
		curPageIndex = 0
		while not self.stop:
			if len(self.storyPages) > 0:
				stories = self.storyPages[0]
				curPageIndex += 1
				del self.storyPages[0]

				print '-------------------第%d页----------------------' %curPageIndex

				curIndex = 0
				for item in stories:
					curIndex += 1
					print u'%d. 作者：' %curIndex +item[0], u'   点赞数：'+item[2]+'\n\n', item[1]+'\n\n',
					if self.voice:
						call(['say', item[1]])
					else:
						input = raw_input()
						self.getNewPage()
						if input == "Q":
							self.stop = True
							return

	#抓取新的一页数据
	def getNewPage(self):
		if not self.stop:
			if len(self.storyPages) <= 1:
				stories = self.analyticalData(self.pageIndex)
				if stories:
					self.storyPages.append(stories)
					self.pageIndex += 1;

	def start(self):
		print '抓取糗事百科，Q退出'
		print '需要自动朗读吗？Y／N'
		while True:
			input = raw_input()
			if input == "Y" or input == "y":
				self.voice = True
				print '已经选择自动朗读，curl + z 退出'
				break;
			elif input == "N" or input == "n":
				self.voice = False
				break;
			else:
				print '只能输入 Y/N'

		self.stop = False
		self.getNewPage()
		self.showStory()

qsbk = QiuShiBaiKe()
qsbk.start()



