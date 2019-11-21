# -*- coding: utf-8
# File : readWord.py 
# Author : baoshan

import docx
from docx import Document
import datetime
import os 

def getfilecontent(basedir):
    '''获取维护文档中表格的内容'''
    paths = getdirfile(basedir)
    f = open('result.txt', 'w')
    for path in paths:
        doc = Document(path)  # 获取文档对象

        tables = doc.tables
        tb = tables[0] # 选取第一个表格
        tb_rows = tb.rows # 表格一共几行
        recordpeople = (tb_rows[1].cells)[1].text # 获取记录人
        recordriqi = (tb_rows[1].cells)[3].text # 获取记录日期
        print(recordpeople, recordriqi) 
        print('*'*100)
        text = (tb_rows[3].cells)[0].text
        print('#'*100)
        print(path)
        print(text)
        f.write('#'*100)
        f.write("\n")
        f.write(path+"\n")
        f.write(text+"\n")
    f.close()



def getdirfile(basedir):
    '''获取文件夹里面的文件名称，和文件夹一起组合成文件'''
    dirlist = getdirlist(basedir)
    absolutefilelist = []
    for dirlist0 in dirlist:
        print('#'*100)
        print(dirlist0)
        for i,j,k in os.walk(dirlist0):
            for k0 in k:
                fileabsolutename = dirlist0 + "\\" +k0  # 文件绝对路径
                absolutefilelist.append(fileabsolutename)
    return absolutefilelist


def getdirlist(basedir):
    '''获取指定文件夹下所有有维护文档的目录'''
    startyear = 2019 # 开始年份
    startyearmonth = 1 # 开始月份
    endyear = datetime.datetime.now().year # 获取当前年份
    endyearmonth = datetime.datetime.now().month # 获取当前月份

    yeardiff = endyear - startyear
    dirlist = []
    for i in range(yeardiff+1):
        baseyear = startyear+i
        if baseyear < endyear:
            for i in range(1,13):
                formatmonth = "{0:02d}".format(i)
                dirlist.append(basedir+"\\"+str(baseyear)+"." +str(formatmonth))
        else:
            for i in range(1, endyearmonth+1):
                formatmonth = "{0:02d}".format(i)
                dirlist.append(basedir + "\\"+ str(baseyear)+"." +str(formatmonth))

    return dirlist


def main():
    basedir = r'D:\0.shenma\0.xxcity\xx智慧城市维护记录'
    getfilecontent(basedir)


if __name__ == "__main__":
    main()

