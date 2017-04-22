from f0 import *
import os
import json

def computeFeatures(dbPath, speakers, outFname=None):
	features = {}

	for speaker, _class in speakers:
		features[_class] = []

	for (speaker,_class) in speakers:
		for fname in os.listdir(dbPath+speaker+"/wav"):
			(speech, f0) = f0estimate(dbPath+speaker+"/wav/"+fname)
			if len(f0) > 0:
				features[_class].append(computeTrajectoryStatistics(f0))
	if outFname is not None:
		with open(outFname, 'w') as f:
			json.dump(features,f)
	return features

from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
import random
def train2NNClassifier(dbPath, speakers, fName=None):
	if fName is None:
		data = computeFeatures(dbPath, speakers)
	else:
		with open(fName, 'r') as f:
			data = json.load(f)
	knn = KNeighborsClassifier()

	dataFemale = np.array(data["female"])
	dataFemaleY = np.array(["female" for i in xrange(dataFemale.shape[0])])
	dataMale = np.array(data["male"])
	dataMaleY = np.array(["male" for i in xrange(dataMale.shape[0])])
	knn.fit(np.concatenate((dataFemale, dataMale)), np.concatenate((dataFemaleY,dataMaleY)))
	return knn

def train3NNClassifier(dbPath, speakers, fName=None):
	if fName is None:
		data = computeFeatures(dbPath, speakers)
	else:
		with open(fName, 'r') as f:
			data = json.load(f)
	knn = KNeighborsClassifier()

	dataFemale = np.array(data["female"])
	dataFemaleY = np.array(["female" for i in xrange(dataFemale.shape[0])])
	dataMale = np.array(data["male"])
	dataMaleY = np.array(["male" for i in xrange(dataMale.shape[0])])
	dataChild = np.array(data["child"])
	dataChildY = np.array(["child" for i in xrange(dataChild.shape[0])])
	knn.fit(np.concatenate((dataFemale, dataMale, dataChild)), np.concatenate((dataFemaleY,dataMaleY,dataChildY)))
	return knn
