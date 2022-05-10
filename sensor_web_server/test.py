import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

x = 0

def button_callback(channel):
    global x
    time.sleep(0.1)
    x += 1
    print(x)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

#GPIO.add_event_detect(40,GPIO.RISING,callback=button_callback,bouncetime=300) # Setup event on pin 10 rising edge
while True:
    if GPIO.input(40) == GPIO.HIGH:
        print("Something is near")

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup()