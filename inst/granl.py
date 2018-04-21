from pyo import *
import random
import math

class Granl:
    def __init__(self, path, numt, numg, mint, maxt, speed, filttype, filtfreq, res):
        self.wantsnew = True
        self.numT = numt
        self.numG = numg
        self.path = path
        self.minT = mint
        self.maxT = maxt
        self.speed = speed
        self.snd = SndTable(path)
        self.env = HannTable(self.snd.getSize(all=False))
        self.pos = Phasor(self.snd.getRate(), 0, self.snd.getSize()).stop()
        self.dur = Noise(.001, .1).stop()
        self.g = Granulator(self.snd, self.env, self.numT, self.pos, self.dur, self.numG).stop()
        self.filt = Biquad(self.g, freq=filtfreq, q=res, type=filttype).stop()
        self.comp = Compress(self.filt, thresh=-30, ratio=8, risetime=0.01, falltime=0.10, lookahead=5.00, knee=0, outputAmp=False).stop()
        self.pan = Pan(self.comp, outs=2, pan=0.50, spread=0.50, mul=0).stop()
        self.pat = Pattern(self.new, self.snd.getDur()/self.speed).stop()
        self.pat2 = Pattern(self.grainShuffle, self.snd.getDur()/self.speed, arg=self.numG).stop()

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self, amp=0.8):
        self.pan.mul = amp
        self.snd.play()
        self.pos.play()
        self.dur.play()
        self.g.play()
        self.filt.play()
        self.comp.play()
        self.pan.play()
        self.pat.play()
        self.pat2.play()

    def stop(self):
        self.pan.mul = 0
        self.snd.stop()
        self.pos.stop()
        self.dur.stop()
        self.g.stop()
        self.filt.stop()
        self.comp.stop()
        self.pan.stop()
        self.pat.stop()
        self.pat2.stop()

    def fadeIn(self, value, time, init=0):
        self.pan.mul = SigTo(value, time, init)

    def fadeOut(self, value, time, init=0.8):
        self.pan.mul = SigTo(value, time, init)

    def new(self):
        self.wantsnew = True
        if self.wantsnew:
            self.randomize(self.pos, self.dur, self.minT, self.maxT, self.pan.pan)
            self.wantsnew = False

    def randomize(self, position, length, mint, maxt, currentPan):
        self.g.pos = position * random.uniform(0.1,1)
        self.g.dur = length * random.uniform(mint, maxt)
        self.transition = SigTo(value=random.uniform(0.2,0.8), time=length, init=currentPan)
        self.pan.pan = self.transition.value

    def grainShuffle(self, numg):
        if numg < 2:
            numg = 2
        self.g.grains = math.floor(random.uniform(numg/2, numg*4))
