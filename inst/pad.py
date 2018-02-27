from pyo import *
import random

class Pad:
    def __init__(self, path, dns=1, pitch=1):
        self.snd = SndTable(path)
        self.end = self.snd.getSize(all=False) - 48000
        self.env = HannTable()
        self.pos = Randi(min=0, max=1, freq=[0.25, 0.3]*10, mul=self.end)
        self.dns = Randi(min=10*dns, max=50*dns, freq=.1)
        self.pit = Randi(min=0.99*pitch, max=1.01*pitch, freq=100)
        self.g = Granule(self.snd, self.env, dens=self.dns, pitch=self.pit, pos=self.pos, dur=0.1)
        self.filt = Biquad(self.g, freq=50, q=2, type=1)
        self.hp = ButHP(self.filt, freq=100)
        self.comp = Compress(self.hp, thresh=-20, ratio=4, risetime=0.01, falltime=0.10, lookahead=5.00, knee=0, outputAmp=False, mul=1)
        self.pan = Pan(self.comp, outs=2, pan=0.50, spread=0.50, mul=0)

    def randomize(self, min, max):
        self.pit.min = random.uniform(min, 2*min)
        self.pit.max = random.uniform(max, 2*max)

    def sideChain(self, str=1, rate=0.5, dur=0.2):
        self.mTrig = Metro(time=rate).play()
        self.tEnv = TrigEnv(self.mTrig, self.env)
        self.clip = Clip(self.tEnv, 1-str, 1)
        self.pan.mul = self.clip

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self, amp=0.8):
        self.pan.mul = amp

    def stop(self):
        self.pan.mul = 0

    def fadeIn(self, value, time, init=0):
        self.pan.mul = SigTo(value, time, init)

    def fadeOut(self, value, time, init=0.8):
        self.pan.mul = SigTo(value, time, init)
