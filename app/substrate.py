from core import *
from numa import *
from bus import *
from sfc import *
import math
import numpy as np


class SubstrateModel:
	def __init__(self):
		self.numaList = []
		self.busList = []
		self.nrNumas = 2
		self.nrCores = 4
		self.busCapacity = 5

	def createNumas(self, nrNumas, nrCores):
		initMemoryCapacity = 50
		initCPU = 10
		for k in range(nrNumas):
			numaID = str(k)
			n = NUMA(numaID, initMemoryCapacity)
			for i in range(nrCores):
				coreID = str(k) + "_" + str(i)
				c = Core(coreID, initCPU, n)
				n.coreList.append(c)
			self.numaList.append(n)

	def createBuses(self):
		for k in range(len(self.numaList)-2):
			b = Bus(self.numaList[k], self.numaList[k+1], self.busCapacity)
			self.busList.append(b)


	def populate(self):
		self.createNumas(self.nrNumas, self.nrCores)
		self.createBuses()	

	def getTotalMemory(self):
		total = 0
		for numa in self.numaList:
			total += numa.memoryCapacity
		return total

	def getTotalCPU(self):
		total = 0
		for numa in self.numaList:
			for cpu in numa.coreList:
				total += cpu.capacity
		return total

	def print(self):
		for numa in self.numaList:
			numa.print()

	def euclidean(self, vnf, numa, cpu):
		if numa.memoryCapacity >= vnf.memoryDemand and cpu.capacity >= vnf.cpuDemand:
			return math.sqrt((numa.memoryCapacity - vnf.memoryDemand)**2 + (cpu.capacity - vnf.cpuDemand)**2)
		else:
			return -1 #doesnt fit

	def l2Norm(self, vnf):
		# distances is a 2d array (because 2 resources are considered)
		# x axis is numas and y axis are their cores
		# so distances[1,1] is the eucl distance between a vnf and numa 1 - core 1
		distances = np.zeros(shape=(len(self.numaList), len(self.numaList[0].coreList))) 
		for x, numa in enumerate(self.numaList):
			for y, cpu in enumerate(numa.coreList):
				dist = self.euclidean(vnf, numa, cpu)
				distances[x,y] = dist
		# print(np.unravel_index(np.argmin(distances), distances.shape))
		if np.amin(distances) != -1:
			return np.unravel_index(np.argmin(distances), distances.shape)
		else:
			return (-1,-1)


	# def partition(self, sfc):
	# 	for vnf in sfc.vnfList:
	# 		bestFit = self.l2Norm(vnf)
	# 		if bestFit != (-1,-1):
	# 			numaIndex = bestFit[0]
	# 			cpuIndex = bestFit[1]
	# 			self.numaList[numaIndex].processWithoutCoreAssignment(vnf)
	# 			self.numaList[numaIndex].coreList[cpuIndex].process(vnf)
	# 		else:
	# 			return False
	# 	return True

	def partition(self, sfc):
		maxLink = -1
		maxBw = -1
		found = False

		for link in sfc.linkList:
			if link.bandwidthDemand > maxBw:
				maxBw = link.bandwidthDemand
				maxLink = link

		vnfs1 = []
		links1 = []
		vnfs2 = []
		links2 = []

		for link in sfc.linkList:
			if not found:
				if link!= maxLink:
					vnfs1.append(link.vnf1)
					vnfs1.append(link.vnf2)
					links1.append(link)
				else:
					found = True
					vnfs1.append(link.vnf1)
					vnfs2.append(link.vnf2)
			else:
				vnfs2.append(link.vnf1)
				vnfs2.append(link.vnf2)
				links2.append(link)

		sfc1ID = sfc.id + "_part1"
		sfc2ID = sfc.id + "_part2"

		sfc1 = SFC(sfc1ID, sfc.duration, sfc.arrivalTime)
		sfc1.vnfList = vnfs1
		sfc1.linkList = links1

		sfc2 = SFC(sfc2ID, sfc.duration, sfc.arrivalTime)
		sfc2.vnfList = vnfs2
		sfc2.linkList = links2

		return [sfc1, sfc2]




