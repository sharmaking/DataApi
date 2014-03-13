#!/usr/bin/python
# -*- coding: utf-8 -*-
# decompress.py
import dataStruct
import copy
import datetime
from decompress_API import decompressData
#api = ctypes.windll.LoadLibrary("./DataApi_64/decompress64.dll")
#解压逐笔成交数据
def DecompressTransactionData(p, nItems):
	pTransactions = dataStruct.getTransactions(nItems)
	nSize = 0
	iData = 0
	nPreTime = 0
	nPreIndex = 0
	nPrePrice = 0
	for i in range(nItems):
		#成交时间
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pTransactions[i]["nTime"] = nPreTime + iData
		nPreTime = pTransactions[i]["nTime"]
		pTransactions[i]["nTime"] = datetime.datetime.strptime(str(nPreTime), "%H%M%S%f").time()
		#成交序号
		nSize = nSize + api.decompressData(iData, p[nSize:])
		nPreIndex = nPreIndex + int(iData)
		pTransactions[i]["nIndex"] = nPreIndex
		#成交价格
		nSize = nSize + api.decompressData(iData, p[nSize:])
		nPrePrice = nPrePrice + int(iData)
		pTransactions[i]["nPrice"] = round(float(nPrePrice)/10000,2)
		#成交数量
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pTransactions[i]["nVolume"] = int(round(iData,-2)/100)

		pTransactions[i]["nTurnover"] = pTransactions[i]["nPrice"] * pTransactions[i]["nVolume"] * 100
	return pTransactions
#解压成交队列
def DecompressOrderQueueData(p, nItems):
	pQueues, pIdnums = dataStruct.getOrderQueue(nItems)
	nSize = 0
	iData = 0
	for i in range(nItems):
		#本日编号
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pIdnums[i] = iData
		#订单编号
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pQueues[i]["nTime"] = datetime.datetime.strptime(str(iData), "%H%M%S%f").time()
		#买卖方向(A:Ask, B:Bid)
		pQueues[i]["nSide"] = p[nSize]
		nSize = nSize + 1
		#订单价格
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pQueues[i]["nPrice"] = round(float(iData)/10000,2)
		#订单数量
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pQueues[i]["nOrders"] = int(iData)
		#队列个数
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pQueues[i]["nABItems"] = int(iData)
		#订单数量
		nABVolume = []
		for k in range(pQueues[i]["nABItems"]):
			nSize = nSize + api.decompressData(iData, p[nSize:])
			nABVolume.append(int(round(iData, -2)/100))
		pQueues[i]["nABVolume"] = nABVolume
	return pQueues, pIdnums
#解压行情数据
def DecompressMarketData(p):
	pMarketData, pIdnum = dataStruct.getMarketData()
	nSize = 0
	iData = 0

	nSize = api.decompressData(iData, p[nSize:])
	pIdnum = iData
	#状态
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nStatus"]	= iData
	#时间
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nTime"]	= datetime.datetime.strptime(str(iData), "%H%M%S%f").time()
	#昨收
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nPreClose"] = round(float(iData)/10000,2)
	#开盘价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nOpen"] = round(float(iData)/10000,2) + pMarketData["nPreClose"]
	#最高价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nHigh"] = round(float(iData)/10000,2) + pMarketData["nPreClose"]
	#最低价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nLow"]  = round(float(iData)/10000,2) + pMarketData["nPreClose"]
	#最新价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nMatch"]= round(float(iData)/10000,2) + pMarketData["nPreClose"]
	#竞买价
	nPrice = pMarketData["nMatch"]
	if not nPrice:
		nPrice = pMarketData["nPreClose"]
	for i in range(10):
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pMarketData["nBidPrice"][i] = nPrice - round(float(iData)/10000,2)
		nPrice = pMarketData["nBidPrice"][i]
	#竞卖价
	nPrice = pMarketData["nMatch"]
	if not nPrice:
		nPrice = pMarketData["nPreClose"]
	for i in range(10):
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pMarketData["nAskPrice"][i] = nPrice - round(float(iData)/10000,2)
		nPrice = pMarketData["nAskPrice"][i]
	#竞买量
	for i in range(10):
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pMarketData["nBidVol"][i] = int(round(iData,-2)/100)
	#竞卖量
	for i in range(10):
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pMarketData["nAskVol"][i] = int(round(iData,-2)/100)
	#成交笔数
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nNumTrades"] = int(iData)
	#成交总量
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["iVolume"]	= int(round(iData,-2)/100)
	#成交总金额
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["iTurnover"]	= iData
	#委托买入总量
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nTotalBidVol"] = int(round(iData,-2)/100)
	#加权平均委买价格
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nWeightedAvgBidPrice"] = round(float(iData)/10000,2)
	#委托卖出总量
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nTotalAskVol"] = int(round(iData,-2)/100)
	#加权平均委卖价格
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nWeightedAvgAskPrice"] = round(float(iData)/10000,2)
	#IOPV净值估值
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nIOPV"] = iData
	#到期收益率
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nYieldToMaturity"] = iData
	#涨停价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nHighLimited"] = pMarketData["nPreClose"] + round(float(iData)/10000,2)
	#跌停价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nLowLimited"] = pMarketData["nPreClose"] + round(float(iData)/10000,2)
	pMarketData["chPrefix"] = p[nSize:nSize+4]
	nSize = nSize + 4;
	return nSize, pMarketData, pIdnum
#解压期货行情数据
def DecompressMarketData_Futures(p):
	pMarketData = dataStruct.getFutureMarketData()
	nSize = 0
	iData = 0

	nSize = api.decompressData(iData, p[nSize:])
	pMarketData["nIndex"]	= iData
	#状态
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nStatus"]	= iData
	#时间
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nTime"]	= datetime.datetime.strptime(str(iData), "%H%M%S%f").time()
	#昨持仓
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["iPreOpenInterest"] = int(iData)
	#前收盘价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nPreClose"] = round(float(iData)/10000,2)
	#昨日结算
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nPreSettlePrice"] = round(float(iData)/10000,2)
	#开盘价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nOpen"] = round(float(iData)/10000,2) + pMarketData["nPreClose"]
	#最高价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nHigh"] = round(float(iData)/10000,2) + pMarketData["nPreClose"]
	#最低价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nLow"]  = round(float(iData)/10000,2) + pMarketData["nPreClose"]
	#最新价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nMatch"]= round(float(iData)/10000,2) + pMarketData["nPreClose"]
	#成交总量
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["iVolume"]	= int(iData)
	#成交总金额
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["iTurnover"] = round(float(iData)/10000,2)
	#持仓
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["iOpenInterest"] = int(iData)
	#收盘价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nClose"] = round(float(iData)/10000,2)
	#结算价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nSettlePrice"] = round(float(iData)/10000,2)
	#涨停价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nHighLimited"] = round(float(iData)/10000,2)
	#跌停价
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nLowLimited"] = round(float(iData)/10000,2)
	#昨虚实度
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nPreDelta"] = iData
	#今虚实度
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nCurrDelta"] = iData
	#竞买价
	nPrice = pMarketData["nMatch"]
	if not nPrice:
		nPrice = pMarketData["nPreClose"]
	for i in range(5):
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pMarketData["nBidPrice"][i] = nPrice - round(float(iData)/10000,2)
		pMarketData["nBidPrice"][i] = round(pMarketData["nBidPrice"][i], 2)
		nPrice = pMarketData["nBidPrice"][i]
	#竞卖价
	nPrice = pMarketData["nMatch"]
	if not nPrice:
		nPrice = pMarketData["nPreClose"]
	for i in range(5):
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pMarketData["nAskPrice"][i] = nPrice - round(float(iData)/10000,2)
		pMarketData["nAskPrice"][i] = round(pMarketData["nBidPrice"][i], 2)
		nPrice = pMarketData["nAskPrice"][i]
	#竞买量
	for i in range(5):
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pMarketData["nBidVol"][i] = int(iData)
	#竞卖量
	for i in range(5):
		nSize = nSize + api.decompressData(iData, p[nSize:])
		pMarketData["nAskVol"][i] = int(iData)
	return nSize, pMarketData
#解压指数数据
def DecompressIndexData(p):
	pMarketData = dataStruct.getIndexMarketData()
	nSize = 0
	iData = 0
	#本日编号
	nSize = api.decompressData(iData, p[nSize:])
	pMarketData["nIndex"] = iData
	#时间
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nTime"]  = datetime.datetime.strptime(str(iData), "%H%M%S%f").time()
	#今日开盘指数
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nOpenIndex"] = round(float(iData)/10000,2)
	#今日最高指数
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nHighIndex"] = round(float(iData)/10000,2) + pMarketData["nOpenIndex"]
	#今日最低指数
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nLowIndex"]  = round(float(iData)/10000,2) + pMarketData["nOpenIndex"]
	#今日最新指数
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nLastIndex"] = round(float(iData)/10000,2) + pMarketData["nOpenIndex"]
	#参与计算相应指数的交易数量
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["iTotalVolume"]	= int(iData)
	#参与计算相应指数的成交金额
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["iTurnover"]	= round(float(iData)/100,2)
	#前收指数
	nSize = nSize + api.decompressData(iData, p[nSize:])
	pMarketData["nPreCloseIndex"] = round(float(iData)/10000,2) + pMarketData["nOpenIndex"]
	return nSize, pMarketData