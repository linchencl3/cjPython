#! /usr/bin/python
# -*- coding:UTF-8 -*-
import sys
import threading
import thread
import time, os, random
reload(sys)
sys.setdefaultencoding("utf8")
import requests
from multiprocessing import Pool,Process,Lock
from xml.dom.minidom import parse
from xml.etree import ElementTree as et;
import json

def urlCount(url):
	count = 0
	headers = {'authorization': '00bee565e80e3caca9762f2e951aff9bbbfe6f2c1cc77ea27b01e83c0c26c11009daaff365986bb510c5970a3126d35b51b93ac653d188bd4b429238c5407f2aa1/00b72ed8c88308f44335b6f7037c41f686c31499871064d3b428535b73e9a87022eb5e1fbb2e412a7acf5624e6790d2476f0aaa2eab77240214cb1d7444957cce5'}
	httpR = requests.get(url,headers=headers)
	httpR.endcoding = 'utf-8'
	string = httpR.text
	root = et.fromstring(string)
	for each in root.getiterator('products'):
		tempDict = each.attrib
		count = tempDict['total-matched']
		count = int(count) / 1000 
		count = count + 1
	return count
	
def urlArr(arr):
	urlArr = []
	cou = len(arr)
	url = '0'
	if cou == 1:
		url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=%d&records-per-page=1000'%(arr[0],1)	
		count = urlCount(url)
		for integer in range(1,count+1):
			url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=%d&records-per-page=1000&'%(arr[0],integer)
			urlArr.append(url)
	
	if cou == 2:
                 priceArr = arr[1]
                 i = 0
		 priceCount = len(priceArr)
                 for num in priceArr:
                	 if i+1 == priceCount:
                        	 url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=1&records-per-page=1000&low-price=%d'%(arr[0],priceArr[i]+1)
				 count = urlCount(url)
				 for integer in range(1,count+1):
					url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=%d&records-per-page=1000&low-price=%d'%(arr[0],integer,priceArr[i]+1)
					urlArr.append(url)
                         else:
                                 url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=1&records-per-page=1000&low-price=%d&high-price=%d'%(arr[0],priceArr[i]+1,priceArr[i+1])
			 	 count = urlCount(url)
				 for integer in range(1,count+1):
				 	url = url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=%d&records-per-page=1000&low-price=%d&high-price=%d'%(arr[0],integer,priceArr[i]+1,priceArr[i+1])
					urlArr.append(url)
				 i = i+1
	if cou == 3:
		priceArr = arr[1]
		i = 0
		priceCount = len(priceArr)
		for num in priceArr:
			if i+1 == priceCount:
				url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=1&records-per-page=1000&currency=%s&low-price=%d'%(arr[0],arr[2],priceArr[i]+1)
				count = urlCount(url)
				for integer in range(1,count+1):
					url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=%d&records-per-page=1000&currency=%s&low-price=%d'%(arr[0],integer,arr[2],priceArr[i]+1)
					urlArr.append(url)
                 	else:
                        	url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=1&records-per-page=1000&currency=%s&low-price=%d&high-price=%d'%(arr[0],arr[2],priceArr[i]+1,priceArr[i+1])
				count = urlCount(url)
				for integer in range(1,count+1):
					url = 'https://product-search.api.cj.com/v2/product-search?website-id=8142637&advertiser-ids=%s&page-number=%d&records-per-page=1000&currency=%s&low-price=%d&high-price=%d'%(arr[0],integer,arr[2],priceArr[i]+1,priceArr[i+1])
					urlArr.append(url)
				i = i + 1
	return urlArr

def httprequest(url,lock,key):
	r = requests.get(url,headers=headers)
        lock.acquire()
	f2 = open('cj%s.json' % key,'a+')
	r.encoding = 'utf-8'
        string = r.text
        root = et.fromstring(string)
        for each in root.getiterator("product"):
        	 tempDict = each.attrib
                 for childNode in each.getchildren():
                	 tempDict[childNode.tag]=childNode.text
		
       		 tempJson = json.dumps(tempDict,ensure_ascii=False)
		 f2.write(tempJson);
      	 	 f2.write(',')
	f2.close()
	lock.release()
	return	

def threadRequest(dic,key):
        print key
	f = open('cj%s.json' % key, 'w+')
	arr = dic[key]
	Arr = urlArr(arr)
	lock = Lock()
	print '%s 得到所有url,总共%d个'%(key,len(Arr))
        f.write('[')
	f.close()
        i = 0
	workers2 = []
        for url in Arr:
		p2 = Process(target = httprequest,args=(url,lock,key))
		#httprequest(url,f)
		p2.start()
		workers2.append(p2)
               #print '%s已经完成%.2f%%'% (key,i*100/len(Arr))
	for p2 in workers2:
		p2.join()
        f.close()
        f = open('cj%s.json' % key,'r+')
        f.seek(-1,2)
        f.write("]")
        f.close()
	print("%s完成"%key)
	return


if __name__ == '__main__':
	dic = {'Yoins':['4507185'],'LUISAVIROMA':['2547997',[-1,1000,2500,5000,10000],'CNY'],'SSENSE':['2125713',[-1,500],'USD'],'stylebop':['3821852',[-1,300,600]],'coggeles':['4721363',[-1,100,200]]}
#dic = {'LUISAVIROMA':['2547997',[-1,1000,2500,5000,10000],'CNY']}
	#print dic.keys()
	headers = {'authorization': '00bee565e80e3caca9762f2e951aff9bbbfe6f2c1cc77ea27b01e83c0c26c11009daaff365986bb510c5970a3126d35b51b93ac653d188bd4b429238c5407f2aa1/00b72ed8c88308f44335b6f7037c41f686c31499871064d3b428535b73e9a87022eb5e1fbb2e412a7acf5624e6790d2476f0aaa2eab77240214cb1d7444957cce5'}
	#dic = {'Yoins':['4507185']}
	workers = []
	for key in dic.keys():
		p = Process(target=threadRequest,args=(dic,key))
		p.start()
		workers.append(p)
	for p in workers:
		p.join()
	print 'OK OK OK OK '

