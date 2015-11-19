# imports

import sys


class Curriculum:

	numCoreReqs = 13;
	numConcReqs = 5;
	
	def __init__(self):
		self.core = [[] for x in xrange(self.numCoreReqs)]
		self.concentration = [] #dummy for now
		self.classList = []

	def add_official_core(self): # still a basic version for testing

		self.core[0].append("symsys100")
		
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

	#def add_to_core(self, class, category):
		# complex logic will go here

	def add_class_list(self, filename):
		file = open(filename, 'r')
		classList = file.readlines()
		for i in range(len(classList)):
			classList[i] = classList[i][:-1]
		print classList
		self.classList = classList

def create_curriculum():
	curriculum = Curriculum()
	curriculum.add_official_core()
	curriculum.printCurriculum()
	curriculum.add_class_list(sys.argv[1])

create_curriculum();