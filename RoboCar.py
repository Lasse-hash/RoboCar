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

sensor_delay = 0.03  

last_direction = "forward" 

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

running = True

delayTime = 0.1

def press(key):
    global running
    if key == "q":
        print("stopping")
        running = False
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
    GPIO.output(dir_left_fwd, True)
    GPIO.output(dir_left_bwd, False)

    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, True)

    pwmL1.ChangeDutyCycle(30)
    pwmL2.ChangeDutyCycle(30)
    pwmR1.ChangeDutyCycle(30)
    pwmR2.ChangeDutyCycle(30)


def turn_left():
    print("Turning LEFT...")
    GPIO.output(dir_left_bwd, False)
    GPIO.output(dir_left_fwd, True)

    GPIO.output(dir_right_fwd, True)
    GPIO.output(dir_right_bwd, False)

    pwmL1.ChangeDutyCycle(65)
    pwmL2.ChangeDutyCycle(65)
    pwmR1.ChangeDutyCycle(65)
    pwmR2.ChangeDutyCycle(85)


def turn_right():
    print("Turning RIGHT...")
    GPIO.output(dir_left_bwd, True)
    GPIO.output(dir_left_fwd, False)

    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, True)

    pwmL1.ChangeDutyCycle(65)
    pwmL2.ChangeDutyCycle(85)
    pwmR1.ChangeDutyCycle(65)
    pwmR2.ChangeDutyCycle(65)


#MAIN LINE LOOP

def line_follow_loop():
    global running
    print("STARTING!")  
    while running:
        
        right = GPIO.input(GPIO_PINV)
        left = GPIO.input(GPIO_PINH)

        time.sleep(sensor_delay)

        right2 = GPIO.input(GPIO_PINV)
        left2 = GPIO.input(GPIO_PINH)
        
        if left != left2 or right != right2:
            if last_direction == "right":
                turn_right()
            elif last_direction == "left":
                turn_left()
            else:
                forward()

        if GPIO.input(GPIO_PINV) == GPIO.LOW and GPIO.input(GPIO_PINH) == GPIO.LOW:
            forward()
            last_direction = "forward"

        elif GPIO.input(GPIO_PINV) == GPIO.HIGH and GPIO.input(GPIO_PINH) == GPIO.HIGH:
            forward()
            time.sleep(0.05)
            last_direction = "forward"
            

        elif GPIO.input(GPIO_PINH) == GPIO.HIGH:
            turn_right()
            time.sleep(0.01)
            last_direction = "right"

        elif GPIO.input(GPIO_PINV) == GPIO.HIGH:
            turn_left()
            time.sleep(0.01)
            last_direction = "left"
        
        else:
            if last_direction == "right":
                turn_right()
            elif last_direction == "left":
                turn_left()
            else:
                forward()

        time.sleep(delayTime)

except KeyboardInterrupt:
    GPIO.cleanup()
    
threading.Thread(
    target=lambda: listen_keyboard(on_press=press),
    daemon=True
).start()

line_follow_loop()





