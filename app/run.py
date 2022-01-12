from request import *
from substrate import *
from schedule import *
import numpy as np


if __name__ == "__main__":
	sub = SubstrateModel()
	req = RequestModel()
	schedule = Schedule()
	sub.populate()
	timehorizon = 20
	AVERAGE=5
	arrivalRate=np.random.poisson(AVERAGE, timehorizon)
	for t in range(timehorizon):
		#check and remove expired services
		schedule.tick(sub)
		schedule.checkForExpiredJobs(sub)
		schedule.removeExpiredJobs(sub)
		for idx in range(arrivalRate[t]):
			id = idx if t < 1 else idx+sum(arrivalRate[:t-1])

			currentSFC = SFC(id, duration=5, arrivalTime=t)
			currentSFC.generate(5)
			print(vars(currentSFC))
			success= schedule.handleRequest(currentSFC, sub)
			if success:
				schedule.tempToAlloc(sub)
			else:
				schedule.cancelAllocations(sub)
			schedule.resetSFC(sub)

			print("\n")






	#requests = req.generate(totalTime)



	# print(requests)
	# print(len(requests))
	# print(sub.numaList)


	#while totalTime > 0:
	#	print(" ****** time left: ", totalTime)
	#	sub.print()
	#	schedule.tick(sub)
	#	schedule.checkForExpiredJobs(sub)
	#	schedule.removeExpiredJobs(sub)

	#	success = schedule.handleRequest(requests.pop(0), sub)
	#	if success:
	#		schedule.tempToAlloc(sub)
	#	else:
	#		schedule.cancelAllocations(sub)
	#	schedule.resetSFC(sub)
	#	totalTime -= 1
	#	print("\n")
