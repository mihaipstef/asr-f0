from lib.f0train import *
import os
import matplotlib.pyplot as plt
from lib.f0 import *

dbPath = "../db/"
#speaker = "cmu_us_bdl_arctic"
trainSpeakers_3class = [ ("cmu_us_slt_arctic", "female"), ("cmu_us_awb_arctic", "male"), ("H26", "child"), ("H27", "child"),
("H28", "child"), ("H29", "child"), ("H30", "child"), ("H31", "child"), ("H32", "child"), ("H33", "child"),
("H34", "child"), ("H35", "child"), ("H36", "child"), ("H37", "child"), ("H38", "child"), ("H39", "child"),
("H40", "child"), ("H41", "child"), ("H42", "child"), ("H43", "child"), ("H44", "child") ]

trainSpeakers_2class = [ ("cmu_us_slt_arctic", "female"), ("cmu_us_awb_arctic", "male") ]

testSpeakers_3class = [ ("cmu_us_clb_arctic", "female"), ("cmu_us_bdl_arctic", "male"), ("H45", "child"), ("H46", "child"),
("H47", "child"), ("H48", "child"),("H49", "child") ,("H50", "child"), ("H51", "child"),
("H52", "child"), ("H53", "child"),  ("H54", "child"), ("H55", "child"),  ("H56", "child"), ("H57", "child"),
("H58", "child"), ("H59", "child"),  ("H60", "child"), ("H61", "child"),  ("H62", "child"), ("H63", "child"),
("H64", "child"), ("H64", "child"),  ("H65", "child"), ("H66", "child"),  ("H67", "child"), ("H68", "child"), ("H69", "child") ]

testSpeakers_2class = [ ("cmu_us_clb_arctic", "female"), ("cmu_us_bdl_arctic", "male") ]

speakers, testSpeakers, trainFunc = trainSpeakers_2class, testSpeakers_2class, train2ClassDTClassifier

#Train
dataFname = "data.json"
if not os.path.isfile(dataFname):
    computeFeatures(dbPath, speakers,dataFname)
classifier = trainFunc(dbPath, speakers,dataFname)

if True:

    #Test
    error = 0
    total = 0
    utt_total = {}
    err = {}
    for (speaker,_class) in testSpeakers:
        for fname in os.listdir(dbPath+speaker+"/wav"):
            (speech, f0) = f0estimate(dbPath+speaker+"/wav/"+fname, 0.5)
            if len(f0) > 0:
                features = computeTrajectoryStatistics(f0)
                total = total + 1
                est_class = classifier.predict(np.array(features).reshape(1,-1))[0]
                if _class != est_class:
                    error = error + 1
                    if (_class, est_class) in err:
                        err[(_class,est_class)] = err[(_class,est_class)] + 1
                    else:
                        err[(_class,est_class)] = 1
                if _class in utt_total:
                    utt_total[_class] = utt_total[_class]+1
                else:
                    utt_total[_class] = 1

    print "Errors: ",error, "No. of utterances: ", total, "Error rate: ", 100 * float(error) / total, "%"

    for (c,est) in err:
        print "{} -> {}: {}%".format(c,est,100*float(err[(c,est)])/utt_total[c])

    print "Test utterances stats"
    for c in utt_total:
        print "{}: {}% ({}/{})".format(c, 100*float(utt_total[c])/total,utt_total[c],total)
