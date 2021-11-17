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
		self.sfcDuration = 7
		self.vlBandwidth = 10

	def generateVNF(self, vnfID, sfcID):
		cpu = random.randint(self.minCpu, self.maxCpu)
		mem = random.randint(self.minMemory, self.maxMemory)
		vnf = VNF(vnfID, cpu, mem, sfcID)
		return vnf

	def generateVirtualLink(self, vlID, vnf1, vnf2, vlBandwidth, sfcID):
		vl = VirtualLink(vlID, vnf1, vnf2, vlBandwidth, sfcID)
		return vl

	def generateSFC(self, sfcID, numberVNFS):
		sfc = SFC(sfcID, self.sfcDuration)
		
		for k in range(numberVNFS):
			vnfID = sfcID + "_" + str(k)
			vnf = self.generateVNF(vnfID, sfc)
			sfc.vnfList.append(vnf)
		
		for k,v in enumerate(sfc.vnfList):
			if k <= len(sfc.vnfList)-2: # dont consider the last vnf
				vl = self.generateVirtualLink(k, sfc.vnfList[k], sfc.vnfList[k+1], self.vlBandwidth, sfcID)
				sfc.linkList.append(vl)
		return sfc


	def generate(self, totalTime):
		vnfNumbers = list(np.random.poisson(self.avgVnfs, totalTime))
		for k,v in enumerate(vnfNumbers):
			sfcID = str(k)
			sfc = self.generateSFC(sfcID,v)
			self.sfcList.append(sfc)
		return self.sfcList
