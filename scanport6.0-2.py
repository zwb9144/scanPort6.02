#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import struct
import threading
import socket
from time import sleep, ctime



#该函数依次扫描每一个port，当该端口开放时输出
def tcp_test(ip,start_port, end_port):

	for target_port in range(start_port, end_port+1):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(6)
		result = sock.connect_ex((ip,target_port))
		if result == 0:
			print "Opened port: port: ",target_port
			#print int2port(target_port)
		sock.close()
#将一个数组分成n个均分的数组的函数,
#传入一个需要分割的次数n，将数据分成N份,最终生成N个列表，将给每个线程使用
def div_group(group,n):

	#group = [192.168.1.1 - 192.168.1.255]
	gs = []
	if len(group)%n == 0:
		for i in range(n):
			gs.append(group[i*(len(group)/n):(i+1)*(len(group)/n)])
	elif len(group)%n != 0:
		for i in range(n):
			if i != n-1:
				gs.append(group[i*(len(group)/n):(i+1)*(len(group)/n)]) 
			else:
				gs.append(group[i*(len(group)/n):])
	return gs

def main():
	# scanip*.py <target_ip> <start_port-- end_port> <线程数>
	#获取需要测试的端口
	if sys.argv[1] == "-h":
		print "useage:  python scanip*.py <target_ip> <start_port-end_port> <number of threads>"
		exit()
	print 'starting at:', ctime()
	target_ip = sys.argv[1]
	#获取线程数
	n = int(sys.argv[3])
	#获取port列表，生成一个数字的范围。 range()函数默认不带最后一个数字，所以加1
	group = range(int(sys.argv[2].split('-')[0]),int(sys.argv[2].split('-')[1])+1)
	# 根据线程数n使用切隔函数将数据切成相应的份数
	gs2=div_group(group,n)
	print gs2
	threads = []


	for j in range(n):
		#传递参数给函数，然后放到线程中
		t = threading.Thread(target=tcp_test,args=(target_ip,gs2[j][0],gs2[j][-1]))
		threads.append(t)

	for j in range(n):
		threads[j].start()

	for j in range(n):
		threads[j].join()

	print "all DONE at:",ctime()

if __name__ == '__main__':
	main()