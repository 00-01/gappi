import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIOs = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

for gpio in GPIOs:
    GPIO.setup(gpio, GPIO.IN)

for gpio in GPIOs:
    print(f"{str(gpio)} : {str(GPIO.input(gpio))}")

# only use to change gpio state
# GPIO.cleanup()