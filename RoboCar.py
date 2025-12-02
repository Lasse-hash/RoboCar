import RPi.GPIO as GPIO
import time

# --- MOTOR A (VENSTRE) ---
A1 = 17
A2 = 18
A3 = 27
A4 = 22

# --- MOTOR B (HØJRE) ---
B1 = 23
B2 = 24
B3 = 25
B4 = 5

GPIO.setmode(GPIO.BCM)
for pin in [A1,A2,A3,A4,B1,B2,B3,B4]:
    GPIO.setup(pin, GPIO.OUT)

seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

delay = 0.002


def step_motor(pins, direction=1, steps=100):
    for _ in range(steps):
        for i in range(8):
            s = i if direction == 1 else 7-i
            GPIO.output(pins[0], seq[s][0])
            GPIO.output(pins[1], seq[s][1])
            GPIO.output(pins[2], seq[s][2])
            GPIO.output(pins[3], seq[s][3])
            time.sleep(delay)


# Kør begge hjul frem
def drive_forward(steps):
    for i in range(steps):
        step_motor([A1,A2,A3,A4], 1, 1)
        step_motor([B1,B2,B3,B4], 1, 1)

# Kør begge hjul tilbage
def drive_backward(steps):
    for i in range(steps):
        step_motor([A1,A2,A3,A4], -1, 1)
        step_motor([B1,B2,B3,B4], -1, 1)

# Drej venstre (højre hjul frem)
def turn_left(steps):
    for i in range(steps):
        step_motor([A1,A2,A3,A4], -1, 1)
        step_motor([B1,B2,B3,B4],  1, 1)

# Drej højre (venstre hjul frem)
def turn_right(steps):
    for i in range(steps):
        step_motor([A1,A2,A3,A4],  1, 1)
        step_motor([B1,B2,B3,B4], -1, 1)


try:
    drive_forward(500)
    time.sleep(1)
    turn_left(300)
    time.sleep(1)
    drive_backward(500)

finally:
    GPIO.cleanup()
