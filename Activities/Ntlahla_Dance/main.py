#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port
from pybricks.tools import wait

ev3 = EV3Brick()

"""
We start by testing the speaker
"""
try: 
    ev3.speaker.beep()
except:
    ev3.screen.draw_text(20, 50, "Eish")

wait(3000)

#---------------------------------
# MUSIC PLAYS WHILE IT MOVES
#------------------

ev3.speaker.play_file("music.wav", wait=False)

#-----------------------
# Watch me move Watch me nay nay music
# -----------------------


