#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket  
import time
import json
import select

remove_cache_timeout_sec =20
max_cache_count =1000

def IpCollector(s):
    ipmap ={}
    s.bind(('0.0.0.0', 19601))
    
    READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR  
    READ_WRITE = READ_ONLY | select.POLLOUT
    poller=select.poll()  
    poller.register(s,READ_ONLY) 
    sfd = s.fileno()
    
    fail=0
    tmsec =time.time()
    while True:
        events = poller.poll(1000)
        
        #检查超时无效的缓存
        if(time.time()-tmsec)%remove_cache_timeout_sec:
            listdel =[]
            for k,v in ipmap.items():
                if time.time()-v["lasttime"]>remove_cache_timeout_sec:
                    listdel.append(k)
            for e in listdel:
                del(ipmap[e])

        for fd,flag in events: #返回的是(fileno,falg)的列表  
            if fd is sfd:
                if flag & (select.POLLIN | select.POLLPRI): 
                    data, addr = s.recvfrom(1024)  
                    if not data:
                        print "client has exist"  
                        continue
                        
                    if data[0:4]=='QUIT':
                        break
                    elif data[0:4]=='GET ':
                        uid =data[4:]
                        if ipmap.has_key(uid):
                            s.sendto(str(ipmap[uid]), addr)
                        else:
                            s.sendto(uid+' not found!', addr)
                        continue
                    else:
                        d =json.loads(data)
                        for k,v in d.items():
                            v["remoteip"] =addr
                            v["lasttime"] =time.time()
                            if len(ipmap)<=max_cache_count:
                                ipmap[k] =v
                                print 'new value:',k,', ',v
                else:  
                    fail = 1  
        if fail:  
            break          
            
if __name__=="__main__":
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        try:
            IpCollector(s)
        except Exception , e:
            print e
        finally:
            s.close()
        time.sleep(4)
        continue
