from pyo import *
import random
import math

class Kick:
    def __init__(self, path, TAPS, TM, w1=90, w2=50, w3=15, transp=1, type=1):
        self.env = CosTable([(0,0),(100,1),(400,.3),(3000,.3),(8191,0)])

        self.mKick = Seq(time=TM, seq=[TAPS], poly=1, onlyonce=False, speed=1)

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self):
        self.pan.mul = 0.8

    def stop(self):
        self.pan.mul = 0

    def fadeIn(self, value, time, init=0):
        self.pan.mul = SigTo(value, time, init)

    def fadeOut(self, value, time, init=0.8):
        self.pan.mul = SigTo(value, time, init)
