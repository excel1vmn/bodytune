from pyo import *

class Fattener:
    def __init__(self, input, speed=1, mul=1):
        self.input = input
        self.speed = speed
        self.mul = mul
        self.fol = Follower(self.input, 10)
        self.lfo = Sine(freq=self.speed, mul=0.5)
        self.dist = Disto(self.input, drive=self.speed, slope=self.fol, mul=mul)
        self.comp = Compress(self.dist, thresh=-20, ratio=4, risetime=0.01, falltime=0.10, lookahead=5.00, knee=0, outputAmp=False, mul=self.fol)
        self.pan = Pan(self.comp, outs=2, pan=0.50, spread=0.50, mul=0)
        self.stop()

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self):
        self.pan.mul = self.mul
        self.fol.play()
        self.lfo.play()
        self.dist.play()
        self.comp.play()
        self.pan.play()

    def stop(self):
        self.pan.mul = 0
        self.fol.stop()
        self.lfo.stop()
        self.dist.stop()
        self.comp.stop()
        self.pan.stop()

    def fadeIn(self, value, time, init=0):
        self.pan.mul = SigTo(value, time, init)

    def fadeOut(self, value, time, init=0.8):
        self.pan.mul = SigTo(value, time, init)
