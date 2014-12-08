#__author__ = 'hefangteng'
#coding:utf-8

import requests
import time
import MySQLdb
import re

def write_to_mysql():
    try:
        cxn = MySQLdb.connect(host='localhost', user='root', passwd='root',db='python')     #与数据库建立连接
    except :
        print "error!"
        exit( 0 )

    cur = cxn.cursor()									    #获取操作游标
    try:
        cur.execute("CREATE TABLE dollar(Local_time VARCHAR(20),USDCNH VARCHAR(8),DINIW  VARCHAR(8))")	#创建一个dollar表，包含记录时间、汇率、美元指数三个参数
    except:
        print 'table dollar exist!'
    try:
        cur.execute("create table oil(Local_time VARCHAR(20),CONC VARCHAR(20))")		    #创建一个oil表，包含记录时间、原油指数两个参数
    except:
        print 'table oil exist!'

    print "数据写入数据库中..."
    while 1:
        value1 = []
        value2 = []
        try :
        	result(value1,value2)							    #调用result函数，获取我们从网页抓取的数据
        except:
            print 'No Values'
        try:
            cur.execute("INSERT INTO dollar VALUES(%s, %s,%s)" ,value1)			    #将对应数据传入dollar表中
        except:
            print 'write to database fail! '
        try:
            cur.execute("INSERT INTO oil VALUES(%s, %s)" ,value2)				    #将对应数据传入oil表中
        except:
            print 'write to database fail!'
        cxn.commit()									    #提交
        time.sleep(60*60)								    #隔一个小时采样一次
    cxn.close()										    #关闭数据库连接

def result(value1,value2):
    url1 = 'http://hq.sinajs.cn/?rn=1417610216083&list=AUDCHF,AUDHKD,AUDJPY,AUDUSD,CADHKD,CADJPY,CHFCAD,CHFHKD,DINIW,EURUSD,GBPEUR,GBPHKD,GBPUSD,USDCAD,USDCHF,USDCNY,USDHKD,USDJPY,gb_dji,gb_ixic,hf_C,hf_CAD,hf_CL,hf_GC,hf_S,hf_SI,int_hangseng,int_nikkei'
    url2 = 'http://hq.sinajs.cn/?rn=1417610565584&list=DINIW'
    url3 = 'http://hq2gjqh.eastmoney.com/em_futures2010numericapplication/index.aspx?type=f&id=CONC0&v=1417613016752&_=1417613016753'

    html1 = requests.get(url1)
    html2 = requests.get(url2)
    html3 = requests.get(url3)

    ISOTIMEFORMAT= '%Y-%m-%d %X'
    value1.append(time.strftime(ISOTIMEFORMAT,time.localtime()))
    value2.append(time.strftime(ISOTIMEFORMAT,time.localtime()))

    USDCNY = re.compile('var hq_str_USDCNY=".*?,(.*?),.*?";').findall(html1.text)
    DINIW = re.compile('".*?,(.*?),.*?";').findall(html2.text)
    CONC = re.compile('extendedFutures:\["0.00,0|0.00,0",".*?,(.*?),.*?"]').findall(html3.text)

    value1.append(USDCNY[0].encode('utf-8'))
    value1.append(DINIW[0].encode('utf-8'))
    value2.append(CONC[1].encode('utf-8'))

if '__name__==__main__':
    write_to_mysql()
