from pyo import *
import random

class ManglerExp:
    def __init__(self, path1, path2, TAPS, TM, drive=1, segments=8, segdur=0.125, w1=100, w2=0, w3=0, poly=1):
        self.path1 = path1
        self.path2 = path2
        self.tm = TM
        self.taps = TAPS
        self.dur1 = sndinfo(self.path1)[1]
        self.dur2 = sndinfo(self.path2)[1]
        self.env = CosTable([(0,0),(32,1),(8100,1),(8191,0)])
        self.tab = SndTable(initchnls=2)
        self.beat = Beat(self.tm, self.taps, w1, w2, w3, poly).play()
        self.transp = self.tab.getRate()
        self.amp = OscTrig(self.env, self.beat, self.tab.getRate())
        self.osc = OscTrig(self.tab, self.beat, self.tab.getRate(), interp=4, mul=2)
        self.fol = Follower(self.osc, freq=20)
        self.dist = Disto(self.osc, drive=drive*self.fol, slope=2)
        self.filt = Biquad(self.dist, 30, q=1, type=1)
        self.panMul = SigTo(0)
        self.panPow = Pow(self.panMul, 3)
        self.pan = Pan(self.filt+self.osc, outs=2, mul=self.panPow)

        self.count = 0
        self.end = TrigFunc(self.beat, self.check)
        self.generate(segments, segdur)
        self.stop()

    def out(self):
        self.pan.out()
        return self

    def sig(self):
        return self.pan

    def play(self, amp=0.8, gen=True):
        self.panMul.value = amp
        self.amp.play()
        self.osc.play()
        self.fol.play()
        self.dist.play()
        self.filt.play()
        self.panMul.play()
        self.panPow.play()
        self.pan.play()
        if gen == True:
            self.end.play()

    def stop(self):
        self.panMul.value = 0
        self.amp.stop()
        self.osc.stop()
        self.fol.stop()
        self.dist.stop()
        self.filt.stop()
        self.pan.stop()
        self.panMul.stop()
        self.panPow.stop()
        self.end.stop()

    def fade(self, value, time):
        self.panMul.time = time
        self.panMul.value = value

    def new(self):
        self.wantsnew = True

    def check(self):
        if self.count == 3:
            self.generate(self.segments, self.segdur)
            self.count = 0
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
                start1 = random.uniform(0, self.dur1-segdur-0.008)
                stop1 = start1 + segdur
                self.tab.append(self.path1, 0.008, start1, stop1)
            else:
                start2 = random.uniform(0, self.dur2-segdur-0.008)
                stop2 = start2 + segdur
                self.tab.append(self.path2, 0.008, start2, stop2)
        newfreq = 1 / (segments * segdur)
        self.amp.freq = newfreq * (self.transp*0.5)
        self.osc.freq = newfreq * (self.transp*0.5)
        self.end.time = 1 / (newfreq * (self.transp*0.5))
