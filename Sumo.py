import RPi.GPIO as GPIO
import time

# Use BCM (Broadcom pin numbering)
GPIO.setmode(GPIO.BCM)

TRIG = 23   # Example GPIO pin for Trigger
ECHO = 24   # Example GPIO pin for Echo

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Ensure trigger is low
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    # Send a 10µs pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for echo end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    # Speed of sound ~34300 cm/s
    distance_cm = pulse_duration * 34300 / 2
    return distance_cm

try:
    while True:
        dist = get_distance()
        if dist > 2 and dist < 450:  # working range of RCWL‑1601 per datasheet
            print(f"Distance: {dist:.1f} cm")
        else:
            print("Out of range")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
