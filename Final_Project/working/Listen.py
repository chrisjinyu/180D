import  speech_recognition  as  sr

P1_INDEX = 3
P2_INDEX = 3



r1 = sr.Recognizer()

def listen(player):
    try:
        if (player == 1):
            print('connecting to p1 mic')
            r1 = sr.Recognizer()
            print("a")
            with  sr.Microphone(device_index=P1_INDEX)  as source:
                print("b")
                r1.adjust_for_ambient_noise(source)
                print('Player one speak')
                audio = r1.listen(source, phrase_time_limit = 2, timeout = 2)
                print('processing...')
                get = r1.recognize_google(audio)
                print(get)
         
        elif (player == 2):
            print('connecting to p2 mic')
            r1 = sr.Recognizer()
            print("b")
            with  sr.Microphone(device_index=P2_INDEX) as source:
                print("c")
                r1.adjust_for_ambient_noise(source)
                print('Player two speak')
                audio = r1.listen(source, phrase_time_limit = 2, timeout = 2)
                print('processing...') 
                get = r1.recognize_google(audio)
                print(get)
                
    except  sr.UnknownValueError:
        print('failed to understand')
    except  sr.RequestError  as e:
        print('failed'.format(e))
 
