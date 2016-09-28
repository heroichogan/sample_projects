#!/usr/bin/env python

# Imports #
import string
import time
import random
import heapq
import shelve


# Constants #
MAX_DELAY = 5   # 5 seconds
MAX_DELAY_PENALTY = 0.3   # 30%
SPLIT_CHAR = '|'
DIRECTORY = 'sets'
FILENAME_ROOT = 'flashCards_3'
OBFUSCATE_RATE = 0.85   # chance obfuscate given word
OBFUSCATE_CHAR = '.'
OBFUSCATE_JOIN_CHAR = ' '
PAD_CHAR = ' '
MAX_LINE_LENGTH = 32
WORRY_ZONE = 0.5



# Score class #
class Score:
    name = None
    value = -88888   
    hits = 0
    misses = 0
    penalty = 0 
    dt = 77777
    
    def __init__( self, name ):
        self.name = name
    
    def __cmp__( self, other ):
        return cmp( self.value, other.value )
    
    def __str__( self ):
        pname = self.name.ljust(MAX_LINE_LENGTH, PAD_CHAR)
        return '%s(%6.2f pts: h=%.2f m=%.2f p=%.2f dt=%.2f)' % (pname, self.value, self.hits, self.misses, self.penalty, self.dt)
        
    def __repr__( self ):
        return self.__str__ ()    # <<<< Could this cause a shelf problem?
   
    def recalculate( self ):
        self.value = self.hits - self.misses + 0.0  # <<<< REPLACE PENALTY


def calcPenalty(dt):
    if dt > MAX_DELAY:
        return MAX_DELAY_PENALTY
    else:
        return 0
    
def obfuscate(text):
    outList = []
    stext = text.split()
    for x in stext:
        if random.random() <= OBFUSCATE_RATE:
            outList.append(OBFUSCATE_CHAR*len(x))
        else:
            outList.append(x)
    return string.join(outList, OBFUSCATE_JOIN_CHAR)
    
def checkAnswer( guess, question, dt, score ):
    s = score[question]
    s.dt = dt
    if guess == matchMap[question]:
        s.hits = s.hits + 1
        s.penalty = s.penalty + calcPenalty(dt)
        s.recalculate()
        return True 
    else:
        s.misses = s.misses + 1
        s.recalculate()
        return False
    
def printScore( score ):
    for x in score:
        print x
    print '- ' * 20


def buildReverseMap(matchMap):
    for x in matchMap.keys():
        matchMap[matchMap[x]] = x


def buildReverseScore(score):
    reverseScore = []
    for x in score.keys():
        heapq.heappush(reverseScore, score[x])
    return reverseScore


def ask( matchMap, reverseScore ):
    question = random.choice(AnswerSelector.getPossibleAnswers(reverseScore))
    t0 = time.clock()
    answer = raw_input('%s (%s) = ' % (question,obfuscate(matchMap[question])) )
    t1 = time.clock()
    return question, answer, t1-t0


# <<<< ADD GRADUAL INTRODUCER HERE
class AnswerSelector:
    @staticmethod
    def getPossibleAnswers(reverseScore):
        return [x.name for x in heapq.nsmallest(int(len(reverseScore)*WORRY_ZONE), reverseScore)]



# Set up answer key 
f = open(DIRECTORY + '/' + FILENAME_ROOT + '.txt')
matchMap = {}
for x in f.readlines():
    line = x.split(SPLIT_CHAR)
    matchMap[line[0].strip()] = line[1].strip()
f.close()

#...and add reverse lookup
buildReverseMap(matchMap)

# Initialize scores
score = {}
for x in matchMap.keys():
    score[x] = Score(x)
    
#...and reverse scores
reverseScore = buildReverseScore(score)
    

# Drill 
question, guess, dt = ask( matchMap, reverseScore )
while guess != 'quitit':
    # Check for a command:
    if guess == 'score':
        printScore( score )
        question, guess, dt = ask( matchMap, reverseScore )
        continue
    elif guess == 'rscore':
        printScore( heapq.nlargest( len(reverseScore), reverseScore ) )
        question, guess, dt = ask( matchMap, reverseScore )
        continue
    elif guess == 'save':
        db = shelve.open(DIRECTORY + '/' + FILENAME_ROOT + '.dat','c')
        for x in matchMap.keys():
            db[x] = score[x]
        db.close()
        print 'Saved.'
        question, guess, dt = ask( matchMap, reverseScore )        
        continue
    elif guess == 'load':
        db = shelve.open(DIRECTORY + '/' + FILENAME_ROOT + '.dat','r')
        score = {}
        for x in db.keys():
            score[x] = db[x]
        reverseScore = buildReverseScore(score)
        db.close()
        print 'Loaded.\n'        
        question, guess, dt = ask( matchMap, reverseScore )
        continue
    elif guess == 'pick5':
        pass #<<<<<
        print 'Picked 5 to drill.\n'
        question, guess, dt = ask( matchMap, reverseScore )
        continue
    
    # Check answer
    if checkAnswer( guess, question, dt, score ):
        print 'Right.'
    else:
        print 'Wrong.'
        print string.swapcase(matchMap[question])
        
    # Print current score for that question
    print '%s.' % score[question]
    
    # Get next guess
    print
    question, guess, dt = ask( matchMap, reverseScore )
    
# See ya #    
print 'Done.'

    
    



