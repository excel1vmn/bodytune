from pyo import *
import random

class Pad:
    def __init__(self, path, TM, dns=1, transp=1, fFreq=150, fRatio=1000, fQ=2, fType=1):
        self.path = path
        self.tm = TM
        self.transp = transp
        self.density = dns
        self.fFreq = SigTo(value=fFreq, time=0.1)
        self.fQ = SigTo(value=fQ, time=0.1)
        if self.fFreq.value <= 1:
            self.fFreq.value = (fFreq.value * fRatio) + 50
        self.snd = SndTable(self.path)
        self.end = self.snd.getSize(all=False) - 48000
        self.env = HannTable()
        self.pos = Randi(min=0, max=1, freq=[0.25, 0.3]*10, mul=self.end)
        self.dns = Randi(min=10*self.density, max=50*self.density, freq=self.tm)
        self.pit = Randi(min=0.99*self.transp, max=1.01*self.transp, freq=100)
        self.g = Granule(self.snd, self.env, dens=self.dns, pitch=self.pit, pos=self.pos, dur=0.1)
        self.hp = Biquad(self.g, freq=self.fFreq, type=fType, q=self.fQ)
        self.panMul = SigTo(0)
        self.panPow = Pow(self.panMul, 3)
        self.pan = Pan(self.hp, outs=2, mul=self.panPow)
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
        self.panMul.value = amp
        self.pos.play()
        self.dns.play()
        self.pit.play()
        self.g.play()
        self.hp.play()
        self.panMul.play()
        self.panPow.play()
        self.pan.play()

    def stop(self):
        self.panMul.value = 0
        self.pos.stop()
        self.dns.stop()
        self.pit.stop()
        self.g.stop()
        self.hp.stop()
        self.panMul.stop()
        self.panPow.stop()
        self.pan.stop()

    def fade(self, value, time):
        self.panMul.time = time
        self.panMul.value = value
