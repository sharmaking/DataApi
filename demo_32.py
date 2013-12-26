#!/usr/bin/python
# -*- coding: utf-8 -*-
from DataApi_32 import CDataApi
import datetime

def main():
	HOST = '192.168.1.186' 
	PORT = 18201
	subStock = ["999999"]

	ApiInstance = CDataApi(HOST,PORT)
	ApiInstance.connectServer()

	ApiInstance.subscibeStock(subStock)
	ApiInstance.requestData(0,1,datetime.datetime(2012,1,1,0,0,0),datetime.datetime(2012,01,1,0,0,0))
	pass

if __name__ == '__main__':
	main()