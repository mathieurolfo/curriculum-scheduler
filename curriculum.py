# imports




class Curriculum:

	numCoreReqs = 13;
	numConcReqs = 5;
	
	def __init__(self):
		self.core = [[] for x in xrange(self.numCoreReqs)]
		self.concentration = [] #dummy for now

	def add_official_core(self):

		self.core[0].append("symsys100")
		
		#skipping complex math requirements here
		self.core[1].append("math51")
		self.core[1].append("cme100")
		self.core[1].append("cme100a")
		self.core[1].append("math51a")
		self.core[1].append("math51h")

	def printCurriculum(self):
		for i in range(self.numCoreReqs):
			print "requirement %(i)i: {" %locals(),
			print str(self.core[i]).strip('[]'),
			print "}"

	def add_to_core(self, class, category):3



def create_curriculum():
	curriculum = Curriculum()
	curriculum.add_official_core()
	curriculum.printCurriculum()

create_curriculum();