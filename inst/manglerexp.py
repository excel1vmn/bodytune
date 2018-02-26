from pyo import *
import random

class ManglerExp:
    def __init__(self, path1, path2, TAPS, TM, panval=0.5, drive=1, segments=8, segdur=0.125, w1=100, w2=0, w3=0, poly=1):
        self.path1 = path1
        self.path2 = path2
        self.dur1 = sndinfo(self.path1)[1]
        self.dur2 = sndinfo(self.path2)[1]
        self.env = CosTable([(0,0),(32,1),(8100,1),(8191,0)])
        self.tab = SndTable(initchnls=2)
        self.beat = Beat(TM, TAPS, w1, w2, w3, poly)
        self.transp = self.tab.getRate()
        self.amp = OscTrig(self.env, self.beat, self.tab.getRate())
        self.osc = OscTrig(self.tab, self.beat, self.tab.getRate(), interp=4, mul=2)
        self.fol = Follower(self.osc, freq=20)
        self.dist = Disto(self.osc, drive=drive*self.fol, slope=2)
        self.filt = Biquadx(self.dist, 30, q=1, type=1)
        self.comp = Compress(self.filt+self.osc, thresh=-24, ratio=6, risetime=.01, falltime=.2, knee=0.3)
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

        start1 = random.uniform(0, self.dur1-segdur)
        stop1 = start1 + segdur
        self.tab.setSound(self.path1, start1, stop1)

        start2 = random.uniform(0, self.dur2-segdur)
        stop2 = start2 + segdur
        self.tab.append(self.path2, start2, stop2)
        for i in range(segments-1):
            i += 1
            if i % 2 == 0:
                start1 = random.uniform(0, self.dur1-segdur-0.004)
                stop1 = start1 + segdur
                self.tab.append(self.path1, 0.002, start1, stop1)
            else:
                start2 = random.uniform(0, self.dur2-segdur-0.004)
                stop2 = start2 + segdur
                self.tab.append(self.path2, 0.002, start2, stop2)
        newfreq = 1 / (segments * segdur)
        self.amp.freq = newfreq * (self.transp*0.5)
        self.osc.freq = newfreq * (self.transp*0.5)
        self.end.time = 1 / (newfreq * (self.transp*0.5))
