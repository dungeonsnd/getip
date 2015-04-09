#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
import time
import sys

def IpAdmin(uid):
    s.sendto("GET "+uid, ('getip-dungeonsnd.rhcloud.com', 19601)  )
    data, addr = s.recvfrom(1024)  
    if not data:
        print "server has exist"  
    else:
        print 'GET result: \n  ',data,'\n'

if __name__=="__main__":
    if len(sys.argv) < 2:
        print 'Usage:%s <uid>'%(sys.argv[0])
        sys.exit(0)
        
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        IpAdmin(sys.argv[1])
    except Exception as e:
        print e
    finally:
        s.close()
