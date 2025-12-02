import RPi.GPIO as GPIO
from time import sleep

from sshkeyboard import listen_keyboard

# --- Left motor ---
pwm_left = 13
dir_left_fwd = 17
dir_left_bwd = 23

# --- Right motor ---
pwm_right = 19
dir_right_fwd = 27
dir_right_bwd = 22

# --- Setup ---
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for pin in [pwm_left, dir_left_fwd, dir_left_bwd,
            pwm_right, dir_right_fwd, dir_right_bwd]:
    GPIO.setup(pin, GPIO.OUT)

# --- PWM objects ---
pwmL = GPIO.PWM(pwm_left, 1000)
pwmR = GPIO.PWM(pwm_right, 1000)

pwmL.start(0)
pwmR.start(0)

# --- Functions to set direction ---
def forward():
    GPIO.output(dir_left_fwd, True)
    GPIO.output(dir_left_bwd, False)

    # Right motor inverted so wheels move the same way
    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, True)

    pwmL.ChangeDutyCycle(100)
    pwmR.ChangeDutyCycle(100)
def backward():
    GPIO.output(dir_left_fwd, False)
    GPIO.output(dir_left_bwd, True)

    # Right motor inverted
    GPIO.output(dir_right_fwd, True)
    GPIO.output(dir_right_bwd, False)

def turnLeft():
    GPIO.output(dir_left_bwd, False)
    GPIO.output(dir_left_fwd, False)

    GPIO.output(dir_right_fwd, True)
    GPIO.output(dir_right_bwd, False)

def turnRight():
    GPIO.output(dir_left_bwd, False)
    GPIO.output(dir_left_fwd, True)
    GPIO.output(dir_right_fwd, False)
    GPIO.output(dir_right_bwd, False)
# --- Run forward with speed ramp ---

def press(key):
    if key == "w":
        forward()
    if key == "a":
        turnLeft()
    if key == "d":
        turnRight()
    if key == "s":
        backward()
while True:
        listen_keyboard(on_press=press)
#try:
 #   while True:
  #      for duty in range(0, 101, 5):
   #         pwmL.ChangeDutyCycle(duty)
    #        pwmR.ChangeDutyCycle(duty)
     #       sleep(0.1)
      #  for duty in range(100, -1, -5):
       #     pwmL.ChangeDutyCycle(duty)
        #    pwmR.ChangeDutyCycle(duty)
         #   sleep(0.1)

#except KeyboardInterrupt:
 #   pwmL.stop()
  #  pwmR.stop()
   # GPIO.cleanup()