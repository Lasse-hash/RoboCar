import RPi.GPIO as GPIO
import time
from sshkeyboard import listen_keyboard
import random
import threading

# Use BCM (Broadcom pin numbering)
GPIO.setmode(GPIO.BCM)
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

GPIO_PINH = 24
GPIO_PINV = 26

turnedback = False

TRIG = 3   # Example GPIO pin for Trigger
ECHO = 2   # Example GPIO pin for Echo

sensor_delay = 0.0005

for pin in [pwm1_left, pwm2_left, dir_left_fwd, dir_left_bwd,
            pwm1_right, pwm2_right, dir_right_fwd, dir_right_bwd]:
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(GPIO_PINH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_PINV, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- PWM objects ---
pwmL1 = GPIO.PWM(pwm1_left, 1000)
pwmL2 = GPIO.PWM(pwm2_left, 1000)
pwmR1 = GPIO.PWM(pwm1_right, 1000)
pwmR2 = GPIO.PWM(pwm2_right, 1000)

pwmL1.start(0)
pwmL2.start(0)
pwmR1.start(0)
pwmR2.start(0)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

running = True

delayTime = 0.005

def press(key):
    global running
    if key == "q":
        print("stopping")
        running = False
        stop()  
        print("STOPPED")
        GPIO.cleanup()      


def stop():
    

    GPIO.output(dir_left_fwd, False)
    GPIO.output(dir_left_bwd, False)
    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, False)

    pwmL1.ChangeDutyCycle(0)
    pwmL2.ChangeDutyCycle(0)
    pwmR1.ChangeDutyCycle(0)
    pwmR2.ChangeDutyCycle(0)

   

    


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

    pwmL1.ChangeDutyCycle(100)
    pwmL2.ChangeDutyCycle(100)
    pwmR1.ChangeDutyCycle(100)
    pwmR2.ChangeDutyCycle(100)


def turn_right():
    print("Turning RIGHT...")

    GPIO.output(dir_left_bwd, True)
    GPIO.output(dir_left_fwd, False)

    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, True)

    pwmL1.ChangeDutyCycle(100)
    pwmL2.ChangeDutyCycle(100)
    pwmR1.ChangeDutyCycle(100)
    pwmR2.ChangeDutyCycle(100)

def turn_back():
    global turnedback

    print("Turning back")

    GPIO.output(dir_left_fwd, False)
    GPIO.output(dir_left_bwd, True)

    # Right motor inverted
    GPIO.output(dir_right_fwd, True)
    GPIO.output(dir_right_bwd, False)

    pwmL1.ChangeDutyCycle(85)
    pwmL2.ChangeDutyCycle(85)
    pwmR1.ChangeDutyCycle(85)
    pwmR2.ChangeDutyCycle(85)
    
    turnedback = False

def slam():
    global turnedback

    print("Slamming")
    
    GPIO.output(dir_left_fwd, True)
    GPIO.output(dir_left_bwd, False)

    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, True)

    pwmL1.ChangeDutyCycle(100)
    pwmL2.ChangeDutyCycle(100)
    pwmR1.ChangeDutyCycle(100)
    pwmR2.ChangeDutyCycle(100)

    turnedback = True

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
    return round(distance_cm, 2)

def Sumo():
    global turnedback
    global running
    print("STARTING!")  
    while running:

        dist = get_distance()

        print(f"distance: {dist}")
        
        right = GPIO.input(GPIO_PINV)
        left = GPIO.input(GPIO_PINH)

        time.sleep(sensor_delay)

        right2 = GPIO.input(GPIO_PINV)
        left2 = GPIO.input(GPIO_PINH)
        
        if left != left2 or right != right2:
            continue  

        if left == GPIO.LOW and right == GPIO.LOW:
            forward()
            if dist <= 20:
                slam()
                
                    
        elif GPIO.input(GPIO_PINV) == GPIO.HIGH:
            stop()
            time.sleep(1)
            turn_right()
            time.sleep(0.02)

        elif GPIO.input(GPIO_PINH) == GPIO.HIGH:
            stop()
            time.sleep(1)
            turn_left()
            time.sleep(0.02)
        elif left == GPIO.HIGH or right == GPIO.HIGH:
            turn_back()
            time.sleep(0.02)

        if turnedback and dist >= 20:
            turn_back()
            time.sleep(0.4)

        time.sleep(delayTime)

threading.Thread(
    target=lambda: listen_keyboard(on_press=press),
    daemon=True
).start()

Sumo()


