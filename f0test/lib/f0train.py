from f0 import *
import os
import json

def computeFeatures(dbPath, speakers, outFname=None):
    features = {}

    for speaker, _class in speakers:
        features[_class] = []

    for (speaker,_class) in speakers:
        for fname in os.listdir(dbPath+speaker+"/wav"):
            (speech, f0, rejects) = f0estimate(dbPath+speaker+"/wav/"+fname)
            if len(f0) > 0:
                features[_class].append(computeTrajectoryStatistics(f0))
                if outFname is not None:
                    with open(outFname, 'w') as f:
                        json.dump(features,f)
    return features

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import datasets
import random

def train2ClassClassifier(classifier, dbPath, speakers, fName=None):
    if fName is None:
        data = computeFeatures(dbPath, speakers)
    else:
        with open(fName, 'r') as f:
            data = json.load(f)

    dataFemale = np.array(data["female"])
    dataFemaleY = np.array(["female" for i in xrange(dataFemale.shape[0])])
    dataMale = np.array(data["male"])
    dataMaleY = np.array(["male" for i in xrange(dataMale.shape[0])])
    classifier.fit(np.concatenate((dataFemale, dataMale)), np.concatenate((dataFemaleY,dataMaleY)))
    return classifier

def train3ClassClassifier(classifier, dbPath, speakers, fName=None):
    if fName is None:
        data = computeFeatures(dbPath, speakers)
    else:
        with open(fName, 'r') as f:
            data = json.load(f)

    dataFemale = np.array(data["female"])
    dataFemaleY = np.array(["female" for i in xrange(dataFemale.shape[0])])
    dataMale = np.array(data["male"])
    dataMaleY = np.array(["male" for i in xrange(dataMale.shape[0])])
    dataChild = np.array(data["child"])
    dataChildY = np.array(["child" for i in xrange(dataChild.shape[0])])
    classifier.fit(np.concatenate((dataFemale, dataMale, dataChild)), np.concatenate((dataFemaleY,dataMaleY,dataChildY)))
    return classifier

def train2ClassKnnClassifier(dbPath, speakers, fName=None):
    knn = KNeighborsClassifier()
    return train2ClassClassifier(knn, dbPath, speakers, fName)

def train3ClassKnnClassifier(dbPath, speakers, fName=None):
    knn = KNeighborsClassifier()
    return train3ClassClassifier(knn, dbPath, speakers, fName)

def train2ClassDTClassifier(dbPath, speakers, fName=None):
    dt = DecisionTreeClassifier()
    return train2ClassClassifier(dt, dbPath, speakers, fName)

def train3ClassDTClassifier(dbPath, speakers, fName=None):
    dt = DecisionTreeClassifier()
    return train3ClassClassifier(dt, dbPath, speakers, fName)
