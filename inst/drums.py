from pyo import *
import random
import math

class Drums:
    def __init__(self, path, TAPS, TM, w1=90, w2=50, w3=15, transp=1, freq=50, type=1, sMul=1):
        self.tm = TM
        self.taps = TAPS
        self.transp = transp
        self.freq = freq
        self.t = CosTable([(0,0),(100,1),(8000,0.7),(8050,0),(8190,0)])
        self.tab = SndTable(path)
        self.beat = Beat(time=self.tm, taps=self.taps, w1=w1, w2=w2, w3=w3, poly=1)
        self.tr2 = TrigEnv(self.beat, table=self.t, dur=self.beat['dur'], mul=self.beat['amp'])
        self.sf = OscTrig(self.tab, self.beat, self.tab.getRate()*self.transp, phase=0, interp=2, mul=1)
        self.filt = Biquad(self.sf, freq=self.freq, q=3, type=type, mul=self.tr2)
        self.comp = Compress(self.filt, thresh=-30, ratio=2, mul=0.5)
        self.fade = SigTo(0, 0.05)
        self.pan = Pan(self.comp, outs=2, pan=0.50, spread=0.50, mul=self.fade)
        self.trig = TrigFunc(self.beat, self.newBeat)
        self.stop()

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self, amp=0.8):
        self.beat.play()
        self.tr2.play()
        self.sf.play()
        self.filt.play()
        self.comp.play()
        self.pan.play()
        self.trig.play()
        self.pan.mul = amp

    def stop(self):
        self.beat.stop()
        self.tr2.stop()
        self.sf.stop()
        self.filt.stop()
        self.comp.stop()
        self.pan.stop()
        self.trig.stop()
        self.pan.mul = 0

    def fadeIn(self, value, time, init=0):
        if self.fade.get() != init:
            self.fade.time = 0
            self.fade.value = init

        self.fade.time = time
        self.fade.value = value

    def fadeOut(self, value, time, init=0.8):
        if self.fade.get() != init:
            self.fade.time = 0
            self.fade.value = init

        self.fade.time = time
        self.fade.value = value

    def newBeat(self):
        self.beat.new()
