import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Pin connected to KY-033 sensor
GPIO_PIN = 24
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

delayTime = 0.5

print("Sensor-Test [press ctrl+c to end]")

try:
    while True:
        if GPIO.input(GPIO_PIN):
            print("LineTracker is on the line")
        else:
            print("LineTracker is not on the line")
        print("---------------------------------------")
        time.sleep(delayTime)

except KeyboardInterrupt:
    GPIO.cleanup()
    