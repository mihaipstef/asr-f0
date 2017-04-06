from lib.f0train import *
import os
import matplotlib.pyplot as plt
from lib.f0 import *

dbPath = "../../db/"
#speaker = "cmu_us_bdl_arctic"
speakers = [ ("cmu_us_slt_arctic", "female"), ("cmu_us_awb_arctic", "male") ]


#computeFeatures(dbPath, speakers,'data.json')


dataFname = "data.json"
if not os.path.isfile(dataFname):
	computeFeatures(dbPath, speakers,dataFname)
classifier = trainKNClassifier(dbPath, speakers,dataFname)


testSpeakers = [ ("cmu_us_clb_arctic", "female"), ("cmu_us_bdl_arctic", "male") ]
error = 0
total = 0
for (speaker,_class) in testSpeakers:
	for fname in os.listdir(dbPath+speaker+"/wav"):
		(speech, f0) = f0estimate(dbPath+speaker+"/wav/"+fname, 0.5)
		if len(f0) > 0:
			features = computeTrajectoryStatistics(f0)
			total = total + 1
			if _class != classifier.predict(np.array(features).reshape(1,-1))[0]:
				error = error + 1

print "Errors: ",error, "No. of utterances: ", total, "Error rate: ", 100 * error / total, "%"
