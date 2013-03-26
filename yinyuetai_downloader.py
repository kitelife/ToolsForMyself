#!/usr/bin/env python
#coding: utf-8

'''

Author: youngsterxyf <sas.198708@gmail.com>

音悦台MV下载器

使用：
    参数：某MV网页的网址
    命令行执行：python yinyuetai_downloader.py [URL]

依赖于第三方库requests来获取网页，你也可以使用urllib2

'''

import re
import sys
import requests
import subprocess


class yinyuetai_downloader(object):

    def __init__(self, url):
        self.page_url = url
        self.page_content = None
        self.download_url = None
        self.video_title = None
        
    def _download_webpage(self):
        r = requests.get(self.page_url)
        if r.status_code == 200:
            self.page_content = r.text

    def _parse_download_url(self):
        download_url_pattern = re.compile("hcVideoUrl\s*:\s*'(.+)'")
        download_url_list = download_url_pattern.findall(self.page_content)
        self.download_url = download_url_list[0]
        print self.download_url

        suffix = self.download_url.split('?')[0].split('.')[-1]
    
        video_title_pattern = re.compile("<h1\s*id=\"videoTitle\">(.+)</h1>")
        video_title_list = video_title_pattern.findall(self.page_content)
        video_title = video_title_list[0].replace(' ', '_')
    
        self.video_title = '{0}.{1}'.format(video_title.encode('utf-8'), suffix)

    def _download_video(self):
        if self.download_url and self.video_title:
            download_cmd_list = ['wget', '-O', self.video_title, self.download_url]
            child = subprocess.Popen(download_cmd_list)
            child.wait()
            print "Finished!"
        else:
            print 'No download_url or video_title'
    
    def download_mv(self):
        self._download_webpage()
        self._parse_download_url()
        self._download_video()


def main():
    page_url = sys.argv[1]
    mv_downloader = yinyuetai_downloader(page_url)
    mv_downloader.download_mv()

if __name__ == '__main__':
    main()
