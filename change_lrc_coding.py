#-*- coding: utf-8 -*-

import chardet #第三方库，下载地址：http://chardet.feedparser.org/download/
import sys
import os

def changeCoding(path):
	for root,dirs,files in os.walk(path):
		for file in files:
			if file.endswith('.lrc'): 
				filepath=root+'/'+file
				print filepath
				fp=open(filepath)
				content=fp.read()
				fp.close()
				detResult=chardet.detect(content)
				coding=detResult['encoding']
				print coding
				if coding == 'utf-8':
					try:
						content=unicode(content,coding).encode('gbk')
						fp=open(filepath,'w')
						fp.write(content)
						fp.close()
					except Exception, e:
						print e.message

if __name__ == '__main__':
	'''
	windows系统的默认编码是gbk/GB2312,而linux系统默认编码是utf-8，所以在两种操作系统之间相互拷贝文件，经常要处理乱码问题，需要进行转码。
	这个程序就是将.lrc歌词文件从utf-8编码转换成gb2312编码。这样winamp的乐辞插件读出来就不是乱码啦。
	'''
	changeCoding(sys.argv[1])
