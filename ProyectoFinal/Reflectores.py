#!/usr/bin/python
# Fecha:            13/Enero/2021
# Descripción:      Contiene funciones para el control de un LED RGB y una tira
#                   de LEDs usando bluedot

from gpiozero import LEDBoard
from math import sqrt

# Atenuación
# Usada para representar a un objeto RGB

class LedRGB:
  # Constructor de la clase
  def __init__(self, bluedot):
    self.bluedot = bluedot
    #                   R   G   B
    self.led = LEDBoard(21, 20, 16, pwm=True)

  # Método que permite asignar atenuaciones distintas a cada componente del RGB
  def set_rgb_color(self,pos):
    # R
    self.led[0].value = - ((sqrt((pos.x**2) + ((pos.y-1)**2)))/2) + 1
    # G
    self.led[1].value = - ((sqrt(((pos.x-0.87)**2) + ((pos.y+0.5)**2)))/2) + 1
    # B
    self.led[2].value = - ((sqrt(((pos.x+0.87)**2) + ((pos.y+0.5)**2)))/2) + 1

  # Método para controlar cuando activar la atuenación
  def control_rgb(self,active):
    if active:
      self.bluedot.when_moved = self.set_rgb_color
    else:
      self.bluedot.when_moved = None
      for i in self.led:
        i.value = 0