import RPi.GPIO as GPIO
from time import sleep

speedPin = 35
DirectionPin = 11

GPIO.cleanup()
GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BCM)
GPIO.setup(speedPin, GPIO.OUT)
GPIO.setup(DirectionPin, GPIO.OUT)


pi_pwm = GPIO.PWM(speedPin, 1000)
pi_pwm.start(0)
GPIO.output(DirectionPin, True)


while True:
    for speed in range(0, 101, 5):
        pi_pwm.ChangeDutyCycle(duty)
        sleep(0.1)
    for speed in range(100, -1, -5):
        pi_pwm.ChangeDutyCycle(duty)
        sleep(0.1)
