import  speech_recognition  as  sr

r1 = sr.Recognizer()
 
def listen(index):
    try:
        if (index == 2):
            print('bose')
            r1 = sr.Recognizer()
            with  sr.Microphone(device_index=2)  as source:
                print('speak mic 2')
                r1.adjust_for_ambient_noise(source)
                audio = r1.listen(source)
                print('processing...')
                get = r1.recognize_google(audio)
                print(get)
         
        elif (index == 3):
            print('v8')
            r1 = sr.Recognizer()
            with  sr.Microphone(device_index=3) as source:
                print('speak mic 3')
                r1.adjust_for_ambient_noise(source)
                audio = r1.listen(source)
                print('processing...') 
                get = r1.recognize_google(audio)
                print(get)
                
    except  sr.UnknownValueError:
        print('failed to understand')
    except  sr.RequestError  as e:
        print('failed'.format(e))
 
 
listen(2)
listen(3)