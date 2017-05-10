from lib.f0train import *

dbPath = "../db/"
speaker = 'lucian'

(speech, f0, rejects) = f0estimate(dbPath+speaker+"/wav/book_meeting_45.wav", 4)
print(speech)
print(f0)
print(rejects)
