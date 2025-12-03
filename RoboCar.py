import RPi.GPIO as GPIO
import time
from sshkeyboard import listen_keyboard

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


GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for pin in [pwm1_left, pwm2_left, dir_left_fwd, dir_left_bwd,
            pwm1_right, pwm2_right, dir_right_fwd, dir_right_bwd]:
    GPIO.setup(pin, GPIO.OUT)

# Pin connected to KY-033 sensor
GPIO_PINH = 24
GPIO_PINV = 26
GPIO.setup(GPIO_PINH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_PINV, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwmL1 = GPIO.PWM(pwm1_left, 1000)
pwmL2 = GPIO.PWM(pwm2_left, 1000)
pwmR1 = GPIO.PWM(pwm1_right, 1000)
pwmR2 = GPIO.PWM(pwm2_right, 1000)

pwmL1.start(0)
pwmL2.start(0)
pwmR1.start(0)
pwmR2.start(0)

delayTime = 0.5

def stop():
    GPIO.output(dir_left_bwd, False)
    GPIO.output(dir_left_fwd, False)

    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, False)

    
    pwmL1.ChangeDutyCycle(0)
    pwmL2.ChangeDutyCycle(0)
    pwmR1.ChangeDutyCycle(0)
    pwmR2.ChangeDutyCycle(0)

def press(key):
    if key == "q":
        stop()

try:
    while True:
        if GPIO.input(GPIO_PINH) == GPIO.HIGH or GPIO.input(GPIO_PINV) == GPIO.HIGH:
            while True:

                pwmL1.ChangeDutyCycle(0)
                pwmL2.ChangeDutyCycle(0)
                pwmR1.ChangeDutyCycle(0)
                pwmR2.ChangeDutyCycle(0)

                #trying to find line again

                if GPIO.input(GPIO_PINH) == GPIO.HIGH:

                    GPIO.output(dir_left_bwd, False)
                    GPIO.output(dir_left_fwd, True)

                    GPIO.output(dir_right_fwd, True)
                    GPIO.output(dir_right_bwd, False)

                    pwmL1.ChangeDutyCycle(20)
                    pwmL2.ChangeDutyCycle(20)
                    pwmR1.ChangeDutyCycle(20)
                    pwmR2.ChangeDutyCycle(20)

                elif GPIO.input(GPIO_PINV) == GPIO.HIGH:
                    GPIO.output(dir_left_bwd, True)
                    GPIO.output(dir_left_fwd, False)

                    GPIO.output(dir_right_fwd, False)
                    GPIO.output(dir_right_bwd, True)

                    pwmL1.ChangeDutyCycle(20)
                    pwmL2.ChangeDutyCycle(20)
                    pwmR1.ChangeDutyCycle(20)
                    pwmR2.ChangeDutyCycle(20)
                if GPIO.input(GPIO_PINH) == GPIO.LOW and GPIO.input(GPIO_PINV) == GPIO.LOW:
                    break

        else:

            GPIO.output(dir_left_fwd, False)
            GPIO.output(dir_left_bwd, True)

            GPIO.output(dir_right_fwd, True)
            GPIO.output(dir_right_bwd, False)

            pwmL1.ChangeDutyCycle(20)
            pwmL2.ChangeDutyCycle(20)
            pwmR1.ChangeDutyCycle(20)
            pwmR2.ChangeDutyCycle(20)

        time.sleep(delayTime)
        listen_keyboard(on_press=press)

except KeyboardInterrupt:
    GPIO.cleanup()
