#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import socketFun
import time

class CDataApi(socket.socket):
	def __init__(self, HOST, PORT):
		super(CDataApi, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
		self.ADDR = (HOST, PORT)
	#链接服务器
	def connectServer(self):
		self.connect(self.ADDR)
		time.sleep(2)
	#订阅股票
	def subscibeStock(self, subStocks):
		socketFun.subscibeStock(self, subStocks)
	#请求数据
	def requestData(self, dataType, flag, startTime, endTime):
		if dataType == 0:		#请求当天数据
			socketFun.requestCurrentDay(self, flag, startTime.time())
		elif dataType == 1:		#请求某一天数据
			socketFun.requestOneDay(self, startTime.date(), startTime.time(), endTime.time())
		elif dataType == 2:		#请求某一段时间数据
			socketFun.requestSomeTimes(self, startTime.date(), endTime.date())
		else:
			print "Request illegal Param"
			return
		socketFun.recvSubscibeRespond(self)