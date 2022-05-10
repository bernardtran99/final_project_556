import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("start")

while True: # Run forever
    if GPIO.input(26) == GPIO.HIGH:
        print("Button 1 was pushed!")
    