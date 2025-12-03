import RPi.GPIO as GPIO
import time
from sshkeyboard import listen_keyboard
import threading

# --- Left motor ---
pwm1_left = 13
pwm2_left = 12
dir_left_fwd = 17
dir_left_bwd = 23

# --- Right motor ---
pwm1_right = 19
pwm2_right = 18
dir_right_fwd = 27
dir_right_bwd = 22

# --- Line sensors ---
GPIO_PINH = 24
GPIO_PINV = 26


# --- GPIO SETUP ---
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

motor_pins = [
    pwm1_left, pwm2_left, dir_left_fwd, dir_left_bwd,
    pwm1_right, pwm2_right, dir_right_fwd, dir_right_bwd
]

for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(GPIO_PINH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_PINV, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PWM setup
pwmL1 = GPIO.PWM(pwm1_left, 1000)
pwmL2 = GPIO.PWM(pwm2_left, 1000)
pwmR1 = GPIO.PWM(pwm1_right, 1000)
pwmR2 = GPIO.PWM(pwm2_right, 1000)

pwmL1.start(0)
pwmL2.start(0)
pwmR1.start(0)
pwmR2.start(0)

delayTime = 0.1

def press(key):

    if key == "q":
        stop()        


def stop():
    

    GPIO.output(dir_left_fwd, False)
    GPIO.output(dir_left_bwd, False)
    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, False)

    pwmL1.ChangeDutyCycle(0)
    pwmL2.ChangeDutyCycle(0)
    pwmR1.ChangeDutyCycle(0)
    pwmR2.ChangeDutyCycle(0)

    print("STOPPED")


def forward():
    GPIO.output(dir_left_fwd, False)
    GPIO.output(dir_left_bwd, True)

    GPIO.output(dir_right_fwd, True)
    GPIO.output(dir_right_bwd, False)

    pwmL1.ChangeDutyCycle(70)
    pwmL2.ChangeDutyCycle(70)
    pwmR1.ChangeDutyCycle(70)
    pwmR2.ChangeDutyCycle(70)


def turn_left():
    print("Turning LEFT...")
    GPIO.output(dir_left_bwd, False)
    GPIO.output(dir_left_fwd, True)

    GPIO.output(dir_right_fwd, True)
    GPIO.output(dir_right_bwd, False)

    pwmL1.ChangeDutyCycle(70)
    pwmL2.ChangeDutyCycle(70)
    pwmR1.ChangeDutyCycle(70)
    pwmR2.ChangeDutyCycle(80)


def turn_right():
    print("Turning RIGHT...")
    GPIO.output(dir_left_bwd, True)
    GPIO.output(dir_left_fwd, False)

    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, True)

    pwmL1.ChangeDutyCycle(70)
    pwmL2.ChangeDutyCycle(80)
    pwmR1.ChangeDutyCycle(70)
    pwmR2.ChangeDutyCycle(70)


#MAIN LINE LOOP

def line_follow_loop():
    print("STARTING!")  
    while True:
        # Read sensors
        left = GPIO.input(GPIO_PINH)
        right = GPIO.input(GPIO_PINV)

        # LOW = sees the line
        if left == GPIO.HIGH and right == GPIO.HIGH:
            forward()

        elif left == GPIO.LOW:
            turn_right()

        elif right == GPIO.LOW:
            turn_left()

        time.sleep(delayTime)
        listen_keyboard(on_press=press)


line_follow_loop()





