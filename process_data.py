#!/usr/bin/python

import sets
import os 

datadir = "./data/"
funcHashSet = set()
funcToCommits = dict()

def addToSet(file):
	with open(file, "r") as f:
		for line in f:
			funcHashSet.add(line)
		

for file in os.listdir(datadir):
	if (file.startswith("hash_")):
		addToSet(datadir + file)

print len(funcHashSet)

for item in funcHashSet:
	print item;

