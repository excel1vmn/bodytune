from pyo import *
import random
import math

class Drums:
    def __init__(self, path, TAPS, TM, w1=90, w2=50, w3=15, transp=1, type=1):
        self.t = CosTable([(0,0),(100,1),(8000,0.9),(8191,0)])
        self.beat = Beat(time=TM, taps=TAPS, w1=w1, w2=w2, w3=w3, poly=1)
        self.tab = SndTable(path)
        self.m = Metro(time=TM*8, poly=1).play()
        self.tr2 = TrigEnv(self.beat, table=self.t, dur=self.beat['dur'], mul=self.beat['amp'])
        self.sf = OscTrig(self.tab, self.beat, self.tab.getRate()*transp, phase=0, interp=2, mul=1)
        self.filt = Biquad(self.sf, freq=40, q=3, type=1, mul=self.tr2)
        self.comp = Compress(self.filt, thresh=-30, ratio=2, mul=0.6)
        self.pan = Pan(self.comp, outs=2, pan=0.50, spread=0.50, mul=0)
        self.trig = TrigFunc(self.m, self.newBeat)

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self, amp=0.8):
        self.pan.mul = amp
        self.beat.play()

    def stop(self):
        self.pan.mul = 0
        self.beat.stop()

    def fadeIn(self, value, time, init=0):
        self.pan.mul = SigTo(value, time, init)

    def fadeOut(self, value, time, init=0.8):
        self.pan.mul = SigTo(value, time, init)

    def newBeat(self):
        self.beat.new()
