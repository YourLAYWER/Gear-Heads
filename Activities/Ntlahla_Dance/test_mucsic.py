#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port
from pybricks.tools import wait

ev3 = EV3Brick()

#Test sound

try: 
    ev3.speaker.play_file("music.wav")
except:
    ev3.screen.draw_text(20, 50, "Eish")