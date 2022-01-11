
class VirtualLink:
	def __init__(self, id, vnf1, vnf2, bandwidthDemand, sfcID):
		self.id = id
		self.vnf1 = vnf1
		self.vnf2 = vnf2
		self.bandwidthDemand = bandwidthDemand
		self.sfcID = sfcID