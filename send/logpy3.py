#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import datetime
import time
import pymysql as mdb
import json
import urllib
import sys
from send import send_mailpy3

#log = "/root/access_" + (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')  + ".log"
#log = "D:\\node1.log"
#line = open(log,'r')
#con = mdb.connect('localhost','','','database',charset="utf8")
#cur = con.cursor()

class check_db(object):
    def __init__(self):
        self.log = "D:\\node1.log"
        
    def check_create(self):
        line = open(self.log,'r')
        error_sql=[]
        try:
            for i in line:
                matchObj = re.match(r'(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,6}Z)(.*)(\d{1,4})(\s)(Query)(\s)(create)(.*)', i, re.I)
                if matchObj != None:
                    time = matchObj.group(1)
                    tread_id = matchObj.group(3)
                    sql = 'create' + matchObj.group(8)
                    error_sql.append([time, tread_id, sql])
                    #print("Time：",time)
                    #print("Tread_id：",tread_id)
                    #print("SQL：",sql)
                    #print('\n')

                    
                    '''
                    ip = matchObj.group(1)
                    #API = "http://ip.taobao.com/service/getIpInfo.php?ip=" + ip
                    jsondata = json.loads(urllib.urlopen(API).read())
                    address = jsondata['data']['country'] + jsondata['data']['region'] + jsondata['data']['city'] + jsondata['data']['isp']
                    time = matchObj.group(2)
                    method = matchObj.group(3)
                    request = matchObj.group(4)
                    status = int(matchObj.group(6))
                    bytesSent = int(matchObj.group(7))
                    request_time = float(matchObj.group(8))
                    refer = matchObj.group(9)
                    agent = matchObj.group(10)
                    cur.execute('insert into nginx_access_log values("%s","%s","%s","%s","%s",%d,%d,%f,"%s","%s")' % (ip,address,time,method,request,status,bytesSent,request_time,refer,agent))
                    '''
        finally:
            line.close()
         #   cur.close()
        return error_sql


if __name__ == '__main__':
    init_check=check_db()
    error_sql=init_check.check_create()
    if error_sql:
        result = str(error_sql)
        print(result)
        print(type(result))
        sentmail=send_mailpy3.SendMail()
        #content=(error_sql,"utf-8")
        title = 'Pyhon检测数据异常'
        sentmail.sendMessage(result, title)
       
    else:
        print('error_sql is  null')
