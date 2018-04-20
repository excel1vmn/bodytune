from pyo import *
import random
import math

class Drums:
    def __init__(self, path, TAPS, TM, w1=90, w2=50, w3=15, transp=1, freq=50, type=1, sMul=1, envTable=[(0,0),(100,1),(8000,0.7),(8050,0),(8190,0)]):
        self.tm = TM
        self.taps = TAPS
        self.transp = transp
        self.freq = freq
        self.sMul = Sig(value=sMul)
        self.t = CosTable(envTable)
        #self.pitchEnv = CosTable([(0,0), (50,1), (150,.25), (300, 0), (8191,0)])
        self.tab = SndTable(path)
        self.beat = Beat(time=self.tm/self.sMul, taps=self.taps, w1=w1, w2=w2, w3=w3, poly=1)
        self.tr2 = TrigEnv(self.beat, table=self.t, dur=self.beat['dur'], mul=self.beat['amp'])
        self.sf = OscTrig(self.tab, self.beat, self.tab.getRate()*self.transp, phase=0, interp=2, mul=1)
        self.filt = Biquad(self.sf, freq=self.freq, q=3, type=type, mul=self.tr2)
        self.panMul = SigTo(0)
        self.panPow = Pow(self.panMul, 3)
        self.pan = Pan(self.filt, outs=2, mul=self.panPow)
        self.trig = TrigFunc(self.beat, self.newBeat)
        self.stop()

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self, amp=0.8):
        self.panMul.value = amp
        self.beat.play()
        self.tr2.play()
        self.sf.play()
        self.filt.play()
        self.panMul.play()
        self.panPow.play()
        self.pan.play()
        self.trig.play()

    def stop(self):
        self.panMul.value = 0
        self.beat.stop()
        self.tr2.stop()
        self.sf.stop()
        self.filt.stop()
        self.panMul.stop()
        self.panPow.stop()
        self.pan.stop()
        self.trig.stop()

    def fade(self, value, time):
        self.panMul.time = time
        self.panMul.value = value

    def newBeat(self):
        self.beat.new()
