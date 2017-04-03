# coding:utf-8
import os
import  urllib2
from lxml import etree
import chardet
# list_dir = os.listdir(os.getcwd())
# print chardet.detect(list_dir[-1])
url =raw_input('Enter the url of video: ')
# http://www.icourses.cn/coursestatic/course_3621.html
# 
def down_load(url):
    urlerror = 1
    while urlerror:
        try:
            fp = urllib2.urlopen(url)
            urlerror = None
        except:
            urlerror = 1

    mybytes = fp.read().decode('utf-8')
# print len(mybytes)
    tree=etree.HTML(mybytes)

    title1=tree.xpath('//div[@class="nav_til"]/div/a/text()')[0].encode('utf-8')
    title=tree.xpath('//div[@class="nav_til"]/div/text()')
# print len(title)

    file_name = ' '.join(title[1].encode('utf-8').split()) + '.flv'.encode('utf-8')
    file_name = ' '.join(file_name.split('\r'))
    new_name =title1.strip() 
    for i in file_name:
        if i:
            new_name  = new_name + i.strip()
        else:
            new_name  = new_name + ' '
    # print new_name

    f = open('tmpt.bat', 'w')
    f.write("@ECHO OFF\nCHCP 65001\nset var=3\n:continue\n: echo 第%var%次循环\n"+'D:\soft\Python35\Scripts\you-get.exe --debug "' + url +'"\nset /a var-=1\nif %var% gtr 0 goto continue\ncls' )
    f.close()
    allt= ['a','b']
    new_name = new_name.decode(chardet.detect(new_name)['encoding']).encode('utf-8')
    while new_name not in allt and new_name:
        os.system('call tmpt.bat')
        try :
            f =open(new_name.decode('utf-8'),'r')
            f.close()
            new_name = ''
        except:
            pass
    print '**********************************************************************************************************************have download one flv file successfully ***************************************************************************************************'
#http://www.icourses.cn/jpk/changeforVideo.action?resId=839392&courseId=3062&firstShowFlag=21http://www.icourses.cn/jpk/changeforVideo.action?resId=839400&courseId=3062&firstShowFlag=21
a = [0,1]
while  a:
    try:
        down_load(url)
        a = []
#         if url[-3]=='=':
#             url = url[:-36] + str(int(url[-37:-31])+4) + url[-31:]
#             print url
#         else:
#             url = url[:-19] + str(int(url[-20:-14]+4)) + url[-19:]
#             print url
    except Exception as e:
        print e
        print 'retrying......................................................................'

# try:
#         down_load(url)
# except Exception as e:
#         print e
#         print 'retrying......................................................................'