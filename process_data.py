#!/usr/bin/python

import sets
import os 

datadir = "./data/"
commitsFile = "./data/commits.txt"

fhashes = set()
functionsToTrack = set()
funcToCommits = dict()
funcToCommitCount = dict()
commits = list()
commitToSeq = dict()
commitToFuncs = dict()
commitToCount = dict()

def setCommitToSeq():
	with open(commitsFile, "r") as f:
		seq = 0
		for line in f:
			commitToSeq[line[0:7]] = seq
			seq += 1
			commits.append(line[0:7])
	commits.reverse()

def setFunctionsToTrack(file):
	with open(file, "r") as f:
		for line in f:
			items = line.split()
			func = items[0]
			functionsToTrack.add(func)

#addToMaps should be called in order of the commits, old to new
def addToMaps(file, commit):
	with open(file, "r") as f:
		for line in f:
			if line not in fhashes:
				fhashes.add(line)
				items = line.split()
				func = items[0]
				fhash = items[1]
				if func in functionsToTrack:
					if funcToCommits.has_key(func):
						funcToCommits[func] = funcToCommits[func] + ',' + commit
						funcToCommitCount[func] += 1
					else:
						funcToCommits[func] = commit
						funcToCommitCount[func] = 0

#creates commitToFunc map. Ignores the functions that are committed only once (never changed)
def makeCommitsToFunc():
	for func, commits in funcToCommits.iteritems():
		commits_arr = commits.split(',')
		if len(commits_arr) > 1:
			for commit in commits_arr:
				if commitToFuncs.has_key(commit):
					commitToFuncs[commit] = commitToFuncs[commit] + ',' + func
					commitToCount[commit] += 1
				else:
					commitToFuncs[commit] = func
					commitToCount[commit] = 1




setCommitToSeq()
#for commit in commits:
#	print '{0} : {1}'.format(commit, commitToSeq[commit])

lastCommitFile = datadir + "hash_" + commits[-1] + ".txt"
setFunctionsToTrack(lastCommitFile)

for commit in commits:
	file = datadir + "hash_" + commit + ".txt"
	addToMaps(file, commit)

makeCommitsToFunc()


f = open('CommitToChangeCount.csv', 'w')
for commit in commits:
	if commitToCount.has_key(commit):
		f.write('{0}, {1}\n'.format(commit, commitToCount[commit]))
f.close()


#for key in commitToFuncs.keys():
#	print key, commitToFuncs[key]

#for key in funcToCommits.keys():
#	print key, funcToCommits[key]

#remove the entries with value 0

#functions = funcToCommitCount.keys()
#functions.sort(lamda x, y: comp(funcToCommitCount[x], funcToCommitCount[y])

sortedFuncs = sorted(funcToCommitCount.iterkeys(), key=lambda k: funcToCommitCount[k], reverse=True)

f = open('FunctionNameToChangeCount.csv', 'w')
for func in sortedFuncs:
	f.write('{0}, {1}\n'.format(func, funcToCommitCount[func]))
f.close()


changeCountToFuncCount = dict()

for func, count in funcToCommitCount.iteritems():
	if changeCountToFuncCount.has_key(count):
		changeCountToFuncCount[count] += 1
	else:
		changeCountToFuncCount[count] = 1

f = open('ChangeCountToFunctionCount.csv', 'w')
for key, value in changeCountToFuncCount.iteritems():
		f.write('{0}, {1}\n'.format(key, value))
f.close()












