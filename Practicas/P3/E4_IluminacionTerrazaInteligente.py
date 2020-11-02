# Fecha:         23/10/2020
# Descripción:   Programa que simula diferentes modos de iluminación en una casa
#                inteligente

#  Modo 0: Control de una lámpara RGB mediante bluedot
#  Modo 1: Encendido automático de luces mediante un sensor de presencia
#  Modo 2: Tira de LEDs controlada por bluedot

from bluedot import BlueDot
from gpiozero import LED
from gpiozero import LEDBoard
from gpiozero import PWMLED
import RPi.GPIO as GPIO
import math
GPIO.setmode(GPIO.BCM)

def set_pos(pos):
    position = (pos.x + 1) / 2
    if (position<0.25):
        tiraLuz.value=(1,0,0,0)
    elif(position<0.5):
        tiraLuz.value=(0,1,0,0)
    elif(position<0.75):
        tiraLuz.value=(0,0,1,0)
    elif(position<1):
        tiraLuz.value=(0,0,0,1)


#Tira de Leds
def tira():
  print("Tira de luz")
  bd.when_moved = set_pos
    
def set_brightness(pos):
    rgb_r.value = - ((math.sqrt((pos.x**2) + ((pos.y-1)**2)))/2) + 1
    rgb_g.value = - ((math.sqrt(((pos.x-0.87)**2) + ((pos.y+0.5)**2)))/2) + 1
    rgb_b.value = - ((math.sqrt(((pos.x+0.87)**2) + ((pos.y+0.5)**2)))/2) + 1

#Led Rgb
def rgb():
    print("Led rgb")
    bd.when_moved = set_brightness

#Led señal de sensor
def sensorMov():
    print("Sensor Mov")
    bd.wait_for_press()
    led.on()
    bd.wait_for_release()
    led.off()

bd = BlueDot()
tiraLuz = LEDBoard(6,13,19,26)
rgb_r = PWMLED(16)
rgb_g = PWMLED(20)
rgb_b = PWMLED(21)
led=LED(22)
GPIO.setup(17,GPIO.IN)
GPIO.setup(27,GPIO.IN)
while True:
  ##Lee entradas del dip
    dip1=GPIO.input(17)
    dip0=GPIO.input(27)
    ##Selección dispositivo
    if (dip1==0 and dip0==0):
        rgb()
    elif (dip1==0 and dip0==1):
        sensorMov()
    else:
        tira()
