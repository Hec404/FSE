from bluedot import BlueDot
from gpiozero import PWMLED
from signal import pause

def set_brightness(pos):
    if pos.y >= 0:
        led_up.value = pos.y
        led_bt.value = 0
    else:
        led_bt.value = -pos.y
        led_up.value = 0
    if pos.x >= 0:
        led_rt.value = pos.x
        led_lf.value = 0
    else:
        led_lf.value = -pos.x
        led_rt.value = 0

led_up = PWMLED(26)
led_bt = PWMLED(19)
led_lf = PWMLED(13)
led_rt = PWMLED(6)

bd = BlueDot()
bd.when_moved = set_brightness

pause()