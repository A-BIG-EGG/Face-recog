import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 20 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    if GPIO.input(20) == GPIO.HIGH:
        print("Button was pushed!")
