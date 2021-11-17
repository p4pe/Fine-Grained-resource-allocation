class SFC:
	def __init__(self, id, duration):
		self.id = id
		self.vnfList = []
		self.linkList = []
		self.duration = duration
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
