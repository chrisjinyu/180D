import speech_recognition as sr

r1=sr.Recognizer()
r1.dynamic_energy_adjustment_ratio =  2
i=1

try:
    with sr.Microphone() as source:
        while i<2:
            r1.adjust_for_ambient_noise(source,duration=5)
            r1.energy_threshold = 4000
            print('Speak something: ')
            audio= r1.listen(source, timeout=5)
            print ("processing...")
            try:
                if 'true' in r1.recognize_google(audio):
                    print('Player said True')
                    i=i+1
                
                if 'false' in r1.recognize_google(audio):
                    print('Player said False')
                    i=i+1 
                else:
                    text=r1.recognize_google(audio)
                    print('You said: {}'.format(text))
            except sr.UnknownValueError:
                print('unknown value error')
            except sr.RequestError as e:
                print('failed'.format(e))
            except sr.WaitTimeoutError:
                print('nothing heard before the timeout')
except sr.UnknownValueError:
    print('unknown value error')
except sr.RequestError as e:
    print('failed'.format(e))
except sr.WaitTimeoutError:
    print('nothing heard before the timeout')

