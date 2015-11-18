import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

# Implement an algorithm that, unlike greedy, finds the optimal word segmentation of an input character sequence. 
# Your algorithm will consider costs based simply on a unigram cost function.
#
# Before jumping into code, you should think about how to frame this problem as a state-space search problem. 
# How would you represent a state? What are the successors of a state? What are the state transition costs? 
# (You don't need to answer these questions in your writeup.)
#
# Uniform cost search (UCS) is implemented for you, and you should make use of it here.[5]
#
# Fill in the member functions of the SegmentationProblem class and the segmentWords function. 
# The argument unigramCost is a function that takes in a single string representing a word and outputs its unigram cost. 
# The function segmentWords should return the segmented sentence with spaces as delimiters, i.e. ' '.join(words). 


class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        # the initial state is your starting string
        return self.query
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return state == ""
        
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        # return all possible moves and the associated costs
        results = []
        for x in range(1, len(state)+1): #can't have a zero character word
            results.append((state[:x], state[x:], self.unigramCost(state[:x])))
        
        return results
        # END_YOUR_CODE

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return ' '.join(ucs.actions)
    # END_YOUR_CODE

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        # our state is the index of current word and the previous word itself. We could use just the index but it complicates the first word
        return (0, wordsegUtil.SENTENCE_BEGIN)
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return state[0] == len(self.queryWords)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        # different path for every word in possibleFills, cost is from bigramCost and takes, tag is the given word
        nextMoves = []
        prevword = state[1]
        queryword = self.queryWords[state[0]]
        if len(self.possibleFills(queryword)) == 0: #no valid reconstructions
            nextMoves.append((queryword, (state[0]+1, queryword), self.bigramCost(prevword, queryword)))
        else:
            for candidateword in self.possibleFills(queryword):
                nextMoves.append( (candidateword, (state[0]+1, candidateword), self.bigramCost(prevword, candidateword)))
        return nextMoves
        # END_YOUR_CODE

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (around 5 lines of code expected)

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return ' '.join(ucs.actions)
    # END_YOUR_CODE

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

#State = ([listOfQueryWords], stringToParse, currentWordIndex, previousWord) \\
#  Actions(s) =  If stringToParse is an empty string, take the query word at the currentWordIndex and investigate all possibleFills. If stringToParse is non-empty, then we will split off a prefix of stringToParse, append it to listOfQueryWords, and parse the rest of stringToParse. \\
#  Cost(s, a) =  the cost of the action is based on the bigram cost model, taking in either previousWord and the candidate from possibleFills or the prefix of stringToParse and the suffix of stringToParse.  \\
#  S\textsubscript{start} = ([], query, 0, wordsegUtil.SENTENCE\_BEGIN)\\
#  isGoal(s) = You know if you've reached the goal state if stringToParse is an empty string and if the currentWordIndex is equal to the length of the listOfQueryWords.



class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return (0, wordsegUtil.SENTENCE_BEGIN)
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return state[0] == len(self.query)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 15 lines of code expected)
        
        currentWordIndex, previousWord = state
        nextMoves = []
        
        for newWordIndex in range(currentWordIndex+1, len(self.query)+1): #for each space insertion   
            queryword = self.query[currentWordIndex:newWordIndex]
            for candidateword in self.possibleFills(queryword): #turn the prefix into a viable word
               
               nextMoves.append((candidateword, (newWordIndex, candidateword), 
                               self.bigramCost(previousWord, candidateword)))
        return nextMoves

        # END_YOUR_CODE

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills))
    return ' '.join(ucs.actions)
    # END_YOUR_CODE

############################################################

if __name__ == '__main__':
    shell.main()
