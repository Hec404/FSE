# Fecha:          09/10/2020
# Descripción:    Semáforo peatonal con botón para que el peatón pida el paso

from gpiozero import LED
from bluedot import BlueDot
from time import sleep

red = LED(17)
green = LED(27)
button = BlueDot()

crosscar = False  # Bandera que indica si ha pedido el paso previamente

while True:
  # ------------------ Estado 1. Sólo rojo encendido. Duración 6seg
  red.on()
  green.off()
  delay = 0.01
  count = 0

  if not crosscar:
    while count < 6:
      sleep(delay)
      count += delay
      if button.is_pressed:
        crosscar = True
        break
  else:
    crosscar = False
    sleep(6)

  # ------------------ Estado 2. Rojo parpadeea. Duración 2seg
  count = 0
  delay = 0.2
  while count < 2:
    red.on()
    sleep(delay)
    red.off()
    sleep(delay)
    count += (delay * 2)
  
  # ------------------ Estado 3. Sólo verde enciende. Duración 6seg
  green.on()
  red.off()
  sleep(6)

  # ------------------ Estado 2. Verde parpadeea. Duración 2seg
  count = 0
  delay = 0.2
  while count < 2:
    green.on()
    sleep(delay)
    green.off()
    sleep(delay)
    count += (delay * 2)
  