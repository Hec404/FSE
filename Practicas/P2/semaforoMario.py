# Fecha:          09/10/2020
# Descripción:    Semáforo con botón para ceder el paso del peatón
 
from gpiozero import LED, Button
from time import sleep
 
red = LED(17)
yellow = LED(27)
green = LED(22)
button = Button(4)
 
crosswalk = False  # Bandera que indica si ha pedido el paso previamente
 
while True:
  # ------------------ Estado 1. Sólo verde encendido. Duración 5seg
  green.on()
  yellow.off()
  red.off()
  delay = 0.01
  count = 0
 
  if not crosswalk:
    while count < 5:
      sleep(delay)
      count += delay
      if button.is_pressed:
        crosswalk = True
        break
  else:
    crosswalk = False
    sleep(5)
 
  # ------------------ Estado 2. Verde parpadea. Duración 2seg
  count = 0
  delay = 0.2
  while count < 2:
    green.on()
    sleep(delay)
    green.off()
    sleep(delay)
    count += (delay * 2)
  
  # ------------------ Estado 3. Sólo amarillo encendido. Duración 2.5seg
  green.off()
  yellow.on()
  sleep(2.5)
 
  # ------------------ Estado 4. Sólo rojo encendido. Duración 5seg
  yellow.off()
  red.on()
  sleep(5)
 
  # ------------------ Estado 5. Rojo y amarillos encendidos
  yellow.on()
  sleep(2)