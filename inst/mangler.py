from pyo import *
import random

class Mangler:
    def __init__(self, path, TAPS, TM, panval=0.5, transp=1, segments=8, segdur=0.125, w1=100, w2=0, w3=0, poly=1, newyork=0):
        self.path = path
        self.transp = transp
        self.dur = sndinfo(self.path)[1]
        self.env = HannTable()
        self.tab = SndTable(initchnls=2)
        self.beat = Beat(TM, TAPS, w1, w2, w3, poly)
        self.amp = OscTrig(self.env, self.beat, self.tab.getRate()*transp)
        self.osc = OscTrig(self.tab, self.beat, self.tab.getRate()*transp, interp=4, mul=4)
        self.fol = Follower(self.osc, freq=20)
        self.filt = Biquadx(self.osc, 30+self.fol*40, q=2, type=1)
        self.bp = Biquadx(self.osc, freq=2000, q=4, type=2, stages=6)
        self.lp = Biquadx(self.bp, freq=1000, q=2, type=0, stages=6, mul=newyork)
        self.comp = Compress(self.filt+self.lp, thresh=-30, ratio=8, risetime=.01, falltime=.2, knee=0.2)
        self.pan = Pan(self.comp, outs=2, pan=panval, mul=0)

        self.count = 0
        self.end = TrigFunc(self.beat, self.check)
        self.generate(segments, segdur)

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self):
        self.pan.mul = 0.8
        self.end.play()
        self.beat.play()

    def stop(self):
        self.pan.mul = 0
        self.end.stop()
        self.beat.play()

    def fadeIn(self, value, time, init=0):
        self.pan.mul = SigTo(value, time, init)

    def fadeOut(self, value, time, init=0.8):
        self.pan.mul = SigTo(value, time, init)

    def new(self):
        self.wantsnew = True

    def check(self):
        if self.count == 3:
            self.generate(self.segments, self.segdur)
        else:
            self.count += 1

    def generate(self, segments=8, segdur=0.125):
        self.segments = segments
        self.segdur = segdur
        start = random.uniform(0, self.dur-segdur)
        stop = start + segdur
        self.tab.setSound(self.path, start, stop)
        for i in range(segments-1):
            start = random.uniform(0, self.dur-segdur)
            stop = start + segdur
            self.tab.append(self.path, 0.002, start, stop)
        newfreq = 1 / (segments * segdur)
        self.amp.freq = newfreq * self.transp
        self.osc.freq = newfreq * self.transp
        self.end.time = 1 / (newfreq * self.transp)
