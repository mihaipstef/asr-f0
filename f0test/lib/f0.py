from sphinxbase.sphinxbase import Yin
import wave
import numpy as np
import ctypes

def f0estimate(wavFile, ltWindowLength=None):

	wv=wave.open(wavFile, 'rb')

	noOfSamples = wv.getnframes()
	windowPeriod = 0.025
	sampleRate = wv.getframerate()
	frameLength = int(sampleRate * windowPeriod)
	noOfFrames = noOfSamples/frameLength
	voiceTh = 0.1
	searchRange = 0.2
	smoothWindow = 2
	f0Max = 350
	f0Min = 85

	#Yin flen, voice_thresh, search_range, smooth_window
	yin = Yin(frameLength,voiceTh, searchRange, smoothWindow)
	yin.start()
	rawData = np.fromstring(wv.readframes(-1), 'Int16');
	data = np.ascontiguousarray(rawData, dtype=np.int16)
	f0s = []
	duration=0
	for i in xrange(noOfFrames):
		if ltWindowLength is not None and duration > ltWindowLength:
			break
		frame = data[i*frameLength:(i+1)*frameLength]
		yin.write(frame)
		result, period, diff = yin.read()
		if result and period > 0:
			pvoice=0
			if diff < 32768:
				pvoice = float(diff) / 32768
				if pvoice > 0.7:
					f0 = float(sampleRate)/period
					if f0 > f0Min and f0 < f0Max:
						duration = duration + windowPeriod
						f0s.append(f0)
	yin.end()
	wv.close()
	return (float(noOfSamples)/sampleRate, f0s)

def computeTrajectoryStatistics(f0s):
	f0s_arr = np.array(f0s)
	f0_mean, f0_std, f0_max, f0_min, f0_median = np.mean(f0s_arr), np.std(f0s_arr), np.max(f0s_arr), np.min(f0s_arr), np.median(f0s_arr)
	return (f0_mean, f0_std, f0_max, f0_min, f0_median)
