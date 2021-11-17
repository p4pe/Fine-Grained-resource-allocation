from request import *
from substrate import *
from schedule import *


if __name__ == "__main__":

	totalTime = 20


	req = RequestModel()
	sub = SubstrateModel()
	schedule = Schedule()


	requests = req.generate(totalTime)
	sub.populate()

	# print(requests)
	# print(len(requests))
	# print(sub.numaList)


	while totalTime > 0:
		print(" ****** time left: ", totalTime)
		sub.print()
		schedule.tick(sub)
		schedule.checkForExpiredJobs(sub)
		schedule.removeExpiredJobs(sub)
		schedule.handleRequest(requests.pop(0), sub)
		schedule.resetSFC(sub)
		totalTime -= 1
		print("\n")
