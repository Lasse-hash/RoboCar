import RPi.GPIO as GPIO
import time
from sshkeyboard import listen_keyboard


afstandssensorTrig = 20
afstandssensorEcho = 16


GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(afstandssensorTrig, GPIO.OUT)
GPIO.setup(afstandssensorEcho, GPIO.OUT)


try:
    while True:
        GPIO.output(afstandssensorTrig, True)
        time.sleep(0.00001)
        GPIO.output(afstandssensorTrig, False)

        while GPIO.input(afstandssensorEcho) == 0:
            pulse_start = time.time()
        
        while GPIO.input(afstandssensorEcho) == 1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        print(f"Distance {distance: .1f} cm")

        time.sleep(0.2)

except KeyboardInterrupt:
    print("Stopping")
    GPIO.cleanup()