from vnf import *
from virtualLink import *
from sfc import *
import numpy as np
import random

class RequestModel:
	def __init__(self):
		self.sfcList = []
		self.avgVnfs = 3
		self.minCpu = 5
		self.maxCpu = 10
		self.minMemory = 5
		self.maxMemory = 10
		self.avgDuration = 7
		self.avgarrivalTime = 5
		self.maxVlBandwidth = 100
		self.minVlBandwidth = 10

	def generateVNF(self, vnfID, sfcID):
		cpu = random.randint(self.minCpu, self.maxCpu)
		mem = random.randint(self.minMemory, self.maxMemory)
		vnf = VNF(vnfID, cpu, mem, sfcID)
		return vnf

	def generateVirtualLink(self, vlID, vnf1, vnf2, vlBandwidth, sfcID):
		vl = VirtualLink(vlID, vnf1, vnf2, vlBandwidth, sfcID)
		return vl

	def generateSFC(self, sfcID, numberVNFS, duration, arrivalTime):
		sfc = SFC(sfcID, duration, arrivalTime)
		
		for k in range(numberVNFS):
			vnfID = sfcID + "_" + str(k)
			vnf = self.generateVNF(vnfID, sfc)
			sfc.vnfList.append(vnf)
		
		for k,v in enumerate(sfc.vnfList):
			if k <= len(sfc.vnfList)-2: # dont consider the last vnf
				vl = self.generateVirtualLink(k, sfc.vnfList[k], sfc.vnfList[k+1], random.randint(self.minVlBandwidth, self.maxVlBandwidth), sfcID)
				sfc.linkList.append(vl)
		return sfc


	def generate(self, totalTime):
		vnfNumbers = list(np.random.poisson(self.avgVnfs, totalTime))
		durationList = list(np.random.poisson(self.avgDuration,totalTime))
		arrivalTimeList = list(np.random.poisson(self.avgarrivalTime, totalTime))
		for k,v,d,a in zip(range(totalTime),vnfNumbers,durationList,arrivalTimeList):
			sfcID = str(k)
			sfc = self.generateSFC(sfcID,v,d,a)
			self.sfcList.append(sfc)
		return self.sfcList
	
