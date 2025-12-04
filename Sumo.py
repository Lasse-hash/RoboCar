import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 20
ECHO = 16

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("Calibrating…")
time.sleep(2)
print("Place the object…")

def get_distance():
    # Send trigger pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)   # 10 microseconds
    GPIO.output(TRIG, False)

    # Wait for echo to go HIGH
    start_time = time.time()
    timeout = start_time + 0.02  # 20ms timeout

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None  # no echo received

    # Wait for echo to go LOW
    timeout = time.time() + 0.02
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # cm

    return round(distance, 2)


try:
    while True:
        d = get_distance()

        if d is None:
            print("⚠ No echo received — sensor not detecting anything")
        else:
            print(f"Distance: {d} cm")

        time.sleep(0.3)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Clean exit")