from pyo import *
import random

class Pad:
    def __init__(self, path, TM, dns=1, transp=1, fFreq=100):
        self.path = path
        self.tm = TM
        self.transp = transp
        self.density = dns
        self.freq = fFreq
        self.snd = SndTable(self.path)
        self.end = self.snd.getSize(all=False) - 48000
        self.env = HannTable()
        self.pos = Randi(min=0, max=1, freq=[0.25, 0.3]*10, mul=self.end)
        self.dns = Randi(min=10*self.density, max=50*self.density, freq=self.tm)
        self.pit = Randi(min=0.99*self.transp, max=1.01*self.transp, freq=100)
        self.g = Granule(self.snd, self.env, dens=self.dns, pitch=self.pit, pos=self.pos, dur=0.1)
        self.hp = ButHP(self.g, freq=self.freq, mul=0.7)
        self.pan = Pan(self.hp, outs=2, pan=0.50, spread=0.50, mul=0)
        self.stop()

    def randomize(self, min, max):
        self.pit.min = random.uniform(min, 2*min)
        self.pit.max = random.uniform(max, 2*max)

    def sideChain(self, str=1, dur=0.2, mul=1):
        self.mTrig = Metro(time=self.tm*mul).play()
        self.tEnv = TrigEnv(self.mTrig, self.env)
        self.clip = Clip(self.tEnv, self.pan.mul-str, 1)
        self.pan.mul = self.clip

    def stopChain(self):
        self.mTrig.stop()
        self.tEnv.stop()

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self, amp=0.8):
        self.pos.play()
        self.dns.play()
        self.pit.play()
        self.g.play()
        self.hp.play()
        self.pan.play()
        self.pan.mul = amp

    def stop(self):
        self.pos.stop()
        self.dns.stop()
        self.pit.stop()
        self.g.stop()
        self.hp.stop()
        self.pan.stop()
        self.pan.mul = 0

    def fadeIn(self, value, time, init=0):
        self.pan.mul = SigTo(value, time, init)

    def fadeOut(self, value, time, init=0.8):
        self.pan.mul = SigTo(value, time, init)

    def updateBPM(self, BPS):
        self.tm = BPS
