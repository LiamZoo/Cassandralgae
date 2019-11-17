###############################################################################
#import generics
###############################################################################
import time
#Import GPIO from raspberry, need pre activation via sudo raspi-config
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


###############################################################################
#import config from local
###############################################################################
import config_motion




def move_raspberry(order):


    ###############################################################################
    #get stuffs from config
    ###############################################################################
    reaction_time = config_motion.giveme['reaction_time']

    step_pin = config_motion.giveme['step_pin']
    dir_pin = config_motion.giveme['dir_pin']
    led_pin = config_motion.giveme['led_pin']



    ###############################################################################
    #prepare GPIO
    ###############################################################################
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup((dir_pin, step_pin, led_pin), GPIO.OUT, initial=GPIO.LOW)

    #Set direction. modify the sign of order if negativ.
    if order > 0:
        GPIO.output(dir_pin, False)
    elif order < 0:
        GPIO.output(dir_pin, True)
        order = -order
    else:
        pass

    #Try to get the led blink pin
    try:
        print("   [i] blink led" + str(led_pin))
        GPIO.output(led_pin, True)
    except ValueError:
        print("   [i] no signal led configured with motor")

    #Loop for number of steps
    n = 0
    while n < order:
        GPIO.output(step_pin, True)

        time.sleep(reaction_time)
        GPIO.output(step_pin, False)

        n = n + 1
    print("[i] did move")
    ###############################################################################
    #clean GPIO
    ###############################################################################
    GPIO.cleanup()



