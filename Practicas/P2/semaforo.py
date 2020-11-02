from gpiozero import LED, Button
from signal import pause
from time import sleep
green = LED(26)
yellow = LED(19)
red = LED(13)

while True:
	red.off()
	yellow.off()
	green.on()
	count = 0
	sleep(5)
	while count < 3:
		green.off()
		sleep(0.5)
		green.on()
		sleep(0.5)
		count += 1
	while count < 6:
		green.off()
		yellow.on()
		sleep(0.5)
		yellow.off()
		sleep(0.5)
		count += 1
	red.on()
	sleep(5)