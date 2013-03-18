#-*- coding: utf-8 -*-

import chardet #第三方库，下载地址：http://chardet.feedparser.org/download/
import os
import argparse


def change_encoding(path, filetype, original_encoding, target_encoding):
    for root,dirs,files in os.walk(path):
        for f in files:
            if f.endswith(filetype): 
                filepath=root+'/'+f
                content = ''
                with open(filepath) as fh:
                    content = fh.read()
                det_result=chardet.detect(content)
                encoding=det_result['encoding'].upper()
                if encoding == original_encoding:
                    try:
                        content = content.decode(original_encoding).encode(target_encoding)
                        with open(filepath, 'w') as fh:
                            fh.write(content)
                        print 'change the encoding of {0} from {1} to {2}'.format(filepath, encoding, target_encoding)
                    except Exception, e:
                        print e.message
                else:
                    print 'the original encoding of {0} is {1}'.format(filepath, encoding)
            else:
                continue


def get_parser():
    arg_parser = argparse.ArgumentParser(description="Tool to change text-file's encoding")
    arg_parser.add_argument('dir', metavar='DIR', help='the directory which contains those files', type=str)
    arg_parser.add_argument('suffix', metavar='SUFFIX', help='the suffix of files whose encoding will be changed', type=str)
    arg_parser.add_argument('-f', '--from', help='the original encoding', type=str)
    arg_parser.add_argument('-t', '--to', help='the target encoding', type=str)

    return arg_parser


if __name__ == '__main__':
    '''
    windows系统的默认编码是gbk/GB2312,而linux系统默认编码是utf-8，
    所以在两种操作系统之间相互拷贝文件，经常要处理乱码问题，需要进行转码。
    '''
    arg_parser = get_parser()
    args = vars(arg_parser.parse_args())
    if not os.path.isdir(args['dir']):
        print 'The directory doesn\'t exist!'
        arg_parser.print_usage()
    else:
        filetype = args['suffix']
        if not filetype.startswith('.'):
            filetype = '.' + filetype
        change_encoding(args['dir'], filetype, args['from'].upper(), args['to'].upper()) 
