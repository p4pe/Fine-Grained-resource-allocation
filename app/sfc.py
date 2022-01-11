import random
from vnf import*
from virtualLink import*
class SFC:
	def __init__(self, id, duration, arrivalTime):
		self.id = id
		self.minCpu = 5
		self.maxCpu = 10
		self.minMemory = 5
		self.maxMemory = 10
		self.maxVlBandwidth = 100
		self.minVlBandwidth = 10
		self.vnfList = []
		self.linkList = []
		self.duration = duration
		self.arrivalTime = arrivalTime
		self.ticked = False

	def getTotalMemory(self):
		total = 0
		for vnf in self.vnfList:
			total += vnf.memoryDemand
		return total

	def getTotalCPU(self):
		total = 0
		for vnf in self.vnfList:
			total += vnf.cpuDemand
		return total

	def generateVNF(self, vnfID, sfcID):
		cpu = random.randint(self.minCpu, self.maxCpu)
		mem = random.randint(self.minMemory, self.maxMemory)
		vnf = VNF(vnfID, cpu, mem, sfcID)
		return vnf

	def generateVirtualLink(self, vlID, vnf1, vnf2, vlBandwidth, sfcID):
		vl = VirtualLink(vlID, vnf1, vnf2, vlBandwidth, sfcID)
		return vl

	def generate(self, numberVNFS):#sfcID numberVNFS, self.duration, self.arrivalTime):
		#sfc = SFC(sfcID, duration, arrivalTime)

		for k in range(numberVNFS):
			vnfID = str(self.id) + "_" + str(k)
			#vnfID = sfcID + "_" + str(k)
			vnf = self.generateVNF(vnfID, self)
			self.vnfList.append(vnf)

		for k, v in enumerate(self.vnfList):
			if k <= len(self.vnfList) - 2:  # dont consider the last vnf
				vl = self.generateVirtualLink(k, self.vnfList[k], self.vnfList[k + 1],
											  random.randint(self.minVlBandwidth, self.maxVlBandwidth), self.id)
				self.linkList.append(vl)
		return self