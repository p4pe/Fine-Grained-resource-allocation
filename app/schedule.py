class Schedule:
	def __init__(self):
		pass

	def assignToSingleNuma(self, sfc, numa, sub):
		for vnf in sfc.vnfList:
			bestFit = sub.l2Norm(vnf)
			numaIndex = bestFit[0]
			cpuIndex = bestFit[1]
			sub.numaList[numaIndex].coreList[cpuIndex].tempAssign(vnf)


	def handleRequest(self, sfc, sub):

		success = True
		print(" ------> SFC ", sfc.id)
		print("SFC total VNFs: ", len(sfc.vnfList))
		print("SFC total memory: ", sfc.getTotalMemory(), "SFC total CPU: ", sfc.getTotalCPU())
		print("Substrate total memory: ", sub.getTotalMemory(), "Substrate total CPU: ", sub.getTotalCPU())

		if sfc.getTotalMemory() > sub.getTotalMemory(): # not enough memory in total
			print("not enough memory. Dropping sfc ", sfc.id)
			return False

		elif sfc.getTotalCPU() > sub.getTotalCPU():	# not enough cpu in total
			print("not enough CPU. Dropping sfc ", sfc.id)	
			return False
		
		else: #search for candidate numas
			candidateNumas = []
			for numa in sub.numaList:
				if numa.memoryCapacity >= sfc.getTotalMemory() and numa.getTotalCPU() >=  sfc.getTotalCPU(): # good candidate
					candidateNumas.append(numa)
			print("found ", len(candidateNumas), " candidate numas.")

			if len(candidateNumas) == 0: # need to partition

				if len(sfc.vnfList) != 1:
					partitions = sub.partition(sfc)
					for part in partitions:
						success = self.handleRequest(part, sub)
				else:
					vnf = sfc.vnfList[0]
					bestFit = sub.l2Norm(vnf)
					if bestFit != (-1,-1):
						numaIndex = bestFit[0]
						cpuIndex = bestFit[1]
						sub.numaList[numaIndex].coreList[cpuIndex].tempAssign(vnf)
					else:
						success = False
			else: # no need to partition. Sort and assign
				success = self.fitInSingleCore(sfc, sub)
				if success:
					print("successfully allocated sfc to single core")
				else:
					sortedCandidates = sorted(candidateNumas, key = lambda x: x.memoryCapacity, reverse = False)
					self.assignToSingleNuma(sfc, sortedCandidates[0], sub)
		return success

	def fitInSingleCore(self, sfc, sub):
		c = sfc.getTotalCPU()
		m = sfc.getTotalMemory()
		
		for numa in sub.numaList:
			if m <= numa.memoryCapacity:
				for cpu in numa.coreList:
					if c <= cpu.capacity:
						for vnf in sfc.vnfList:
							cpu.tempAssign(vnf)
						return True
		return False

	def cancelAllocations(self, sub):
		for numa in sub.numaList:
			numa.cancelAllocations()

	def removeExpiredJobs(self, sub):
		for numa in sub.numaList:
			numa.removeExpiredJobs()

	def checkForExpiredJobs(self, sub):
		for numa in sub.numaList:
			for core in numa.coreList:
				for vnf in core.vnfList:
					if vnf.sfc.duration == 0:
						print("VNF ", vnf.id, " of SFC ", vnf.sfc.id, " has expired. Removing from Numa ", numa.id)
						core.removeVNF(vnf)
						numa.removeVNF(vnf)

	def tick(self, sub):
		for numa in sub.numaList:
			for core in numa.coreList:
				for vnf in core.vnfList:
					if not vnf.sfc.ticked:
						vnf.sfc.duration -= 1
						vnf.sfc.ticked = True 

	def resetSFC(self, sub):
		for numa in sub.numaList:
			for core in numa.coreList:
				core.clearExpiredJobs()
				for vnf in core.vnfList:
					vnf.sfc.ticked = False

	def tempToAlloc(self, sub):
		for numa in sub.numaList:
			numa.tempToAlloc()









		
