class NUMA:
	def __init__(self, id, initMemoryCapacity):
		self.id = id
		self.initMemoryCapacity = initMemoryCapacity
		self.memoryCapacity = initMemoryCapacity
		self.coreList = []

	def getTotalCPU(self):
		total = 0
		for c in self.coreList:
			total += c.capacity
		return total

	def assignVnfToCore(self, vnf):
		for core in self.coreList:
			if vnf.cpuDemand <= core.capacity:
				core.process(vnf)
				break;

	def process(self, vnf):
		self.memoryCapacity -= vnf.memoryDemand
		self.assignVnfToCore(vnf)

	def processWithoutCoreAssignment(self, vnf):
		self.memoryCapacity -= vnf.memoryDemand

	def removeVNF(self, vnf):
		self.memoryCapacity += vnf.memoryDemand

	def printVNFS(self):
		for core in self.coreList:
			core.printVNFS()

	def print(self):
		print("numa ", self.id, " memory: ", self.memoryCapacity, " cpu: ", self.getTotalCPU())
		self.printVNFS()

	def cancelAllocations(self):
		for core in self.coreList:
			core.cancelAllocations()

	def removeExpiredJobs(self):
		for core in self.coreList:
			core.removeExpiredJobs()


	def tempToAlloc(self):
		for core in self.coreList:
			core.tempToAlloc()
