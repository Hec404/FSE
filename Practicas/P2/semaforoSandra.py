from gpiozero import LED,Button
from signal import pause
from time import sleep

green = LED(26)
yellow = LED(19)
red = LED(13)
boton = Button(6)
bandera = 0

def rojo():
	red.on()
	print("Paso peatón")
	sleep(6)

def amarillo():
	count = 0
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
	rojo()

while True:
	bandera = 0
	for i in range(10):
		red.off()
		yellow.off()
		green.on()
		sleep(1)
		if boton.is_pressed:
			if bandera == 0:
				print("Ceder paso")
				bandera = 1
				amarillo()
			else:
				print("Lo siento, espere")
	amarillo()
	rojo()