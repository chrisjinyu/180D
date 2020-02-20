import  speech_recognition  as  sr

P1_INDEX = 1
P2_INDEX = 1

r1 = sr.Recognizer()

def listen(player):
	try:
		if (player == 1):
			#print('bose')
			r1 = sr.Recognizer()
			with  sr.Microphone(device_index=P1_INDEX)  as source:
				r1.adjust_for_ambient_noise(source)
				print('Player one speak')
				audio = r1.listen(source)
				print('processing...')
				get = r1.recognize_google(audio)
				return get
				#print(get)
		 
		elif (player == 2):
			#print('v8')
			r1 = sr.Recognizer()
			with  sr.Microphone(device_index=P2_INDEX) as source:
				r1.adjust_for_ambient_noise(source)
				print('Player two speak')
				audio = r1.listen(source)
				print('processing...') 
				get = r1.recognize_google(audio)
				return get
				#print(get)
				
	except  sr.UnknownValueError:
		print('failed to understand')
		return "null"
		#return "null"
	except  sr.RequestError  as e:
		return "null"
		print('failed'.format(e))
		#return "null"
	#finally:
		#return "null"
