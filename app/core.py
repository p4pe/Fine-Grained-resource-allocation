class Core:
	def __init__(self, id, initCapacity, numa):
		self.id = id
		self.initCapacity = initCapacity
		self.numa = numa
		self.capacity = initCapacity
		self.vnfList = []
		self.expiredJobs = []

	def process(self, vnf):
		self.vnfList.append(vnf)
		self.capacity -= vnf.cpuDemand

	def removeVNF(self, vnf):
		self.expiredJobs.append(vnf)
		self.capacity += vnf.cpuDemand

	def removeExpiredJobs(self):
		for exp in self.expiredJobs:
			print("expired job id: ", exp.id)
			self.printVNFS()
			self.vnfList.remove(exp)

	def printVNFS(self):
		for vnf in self.vnfList:
			print("\tcore ", self.id, " running VNF ", vnf.id)

	def clearExpiredJobs(self):
		self.expiredJobs = []
