import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        GPIO.output(TRIG, False)
        #print "Waiting for sensor to settle"
        time.sleep(1)

        GPIO.output(TRIG, True)           #sending pulse that will bounce off object to be measured
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:        #timing how long sound wave takes to return
            pulse_start = time.time()
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        inchDist = distance/2.54
        
        print ("Distance: %.2f cm\t %.2f in" %(distance, inchDist))

except KeyboardInterrupt:
    print("Cleaning up")
    GPIO.cleanup()
