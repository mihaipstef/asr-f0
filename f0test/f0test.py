from lib.f0 import *

dbPath = "../../db/"
#speaker = "cmu_us_bdl_arctic"
speaker = "cmu_us_slt_arctic"
file = "arctic_a0001.wav"
#dbPath+speaker+"/wav/"+file

import os
count = 0
f0s = []
totalSpeech = 0
for fname in os.listdir(dbPath+speaker+"/wav"):
	count = count+1
	(speech, f0) = f0estimate(dbPath+speaker+"/wav/"+fname)
	f0s = f0s + f0
	totalSpeech = totalSpeech + speech
	if count > 50:
		break

print computeTrajectoryStatistics(f0s), totalSpeech/60
