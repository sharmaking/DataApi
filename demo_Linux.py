#!/usr/bin/python
# -*- coding: utf-8 -*-
from DataApi_Linux import CDataProcess
import datetime

def main():
	#HOST = '192.168.1.186'
	HOST = '180.166.168.126'	#公网ip
	PORT = 18202
	subStock = ["999999"]

	ApiInstance = CDataProcess(HOST,PORT,
		False, subStock,
		0,1,datetime.datetime(2012,1,1,0,0,0),datetime.datetime(2012,01,1,0,0,0)
		)
	ApiInstance.run()
	pass

if __name__ == '__main__':
	main()