#!/usr/bin/python

import sets
import os 

datadir = "./data/"

fhashes = set()
funcToCommits = dict()
funcToCounts = dict()
commitToFuncs = dict()

#addToMaps should be called in order of the commits, old to new
def addToMaps(file, commit):
	with open(file, "r") as f:
		for line in f:
			if line not in fhashes:
				fhashes.add(line)
				items = line.split()
				func = items[0]
				fhash = items[1]
				if funcToCommits.has_key(func):
					funcToCommits[func] = funcToCommits[func] + ',' + commit
					funcToCounts[func] = funcToCounts[func] + 1;
				else:
					funcToCommits[func] = commit
					funcToCounts[func] = 0;

#creates commitToFunc map. Ignores the functions that are committed only once (never changed)
def makeCommitsToFunc():
	for func, commits in funcToCommits.iteritems():
		commits_arr = commits.split(',')
		if len(commits_arr) > 1:
			for commit in commits_arr:
				if commitToFuncs.has_key(commit):
					commitToFuncs[commit] = commitToFuncs[commit] + ',' + func
				else:
					commitToFuncs[commit] = func


for file in os.listdir(datadir):
	if file.startswith("hash_"):
		addToMaps(datadir + file, file[5:-4])

makeCommitsToFunc()

#for key in commitToFuncs.keys():
#	print key, commitToFuncs[key]

#for key in funcToCommits.keys():
#	print key, funcToCommits[key]


#remove the entries with value 0
funcToCounts1 = dict((k, v) for k, v in funcToCounts.items() if v > 0)
sortedFuncs = sorted(funcToCounts1.iterkeys(), key=lambda k: funcToCounts1[k])

#sortedFuncs = sorted(funcToCounts.iterkeys(), key=lambda k: funcToCounts1[k])

for func in sortedFuncs:
	print '{0} : {1}'.format(func, funcToCounts[func])


