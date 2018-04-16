from pyo import *
import random

class Mangler:
    def __init__(self, path, TAPS, TM, transp=1, segments=8, segdur=0.125, w1=100, w2=0, w3=0, poly=1, newyork=0):
        self.path = path
        self.tm = TM
        self.taps = TAPS
        self.transp = transp
        self.dur = sndinfo(self.path)[1]
        self.env = HannTable()
        self.tab = SndTable(initchnls=2)
        #self.tab = [SndTable(initchnls=2), SndTable(initchnls=2)]
        self.playing = 0
        self.beat = Beat(self.tm, self.taps, w1, w2, w3, poly).play()
        self.amp = OscTrig(self.env, self.beat, self.tab.getRate()*transp)
        self.osc = OscTrig(self.tab, self.beat, self.tab.getRate()*transp, interp=4, mul=2)
        self.amp2 = OscTrig(self.env, self.beat, self.tab.getRate()*transp)
        self.osc2 = OscTrig(self.tab, self.beat, self.tab.getRate()*transp, interp=4, mul=2)
        self.fol = Follower(self.osc, freq=20)
        self.filt = Biquad(self.osc, 30+self.fol*40, q=2, type=1)
        self.bp = ButBP(self.osc, freq=2000, q=4)
        self.lp = Biquad(self.bp, freq=1000, q=2, type=0, mul=newyork)
        self.panMul = SigTo(0)
        self.panPow = Pow(self.panMul, 3)
        self.pan = Pan(self.filt+self.lp, outs=2, mul=self.panPow)

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
        self.filt.play()
        self.bp.play()
        self.lp.play()
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
        self.filt.stop()
        self.bp.stop()
        self.lp.stop()
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
        else:
            self.count += 1

    def generate(self, segments=8, segdur=0.125):
        self.segments = segments
        self.segdur = segdur
        start = random.uniform(0, self.dur-segdur-0.1)
        stop = start + segdur
        self.tab.setSound(self.path, start, stop)
        for i in range(segments-1):
            start = random.uniform(0, self.dur-segdur-0.1)
            stop = start + segdur
            self.tab.append(self.path, 0.1, start, stop)
        newfreq = 1 / (segments * segdur)
        self.amp.freq = newfreq * self.transp
        self.osc.freq = newfreq * self.transp
        self.end.time = 1 / (newfreq * self.transp)
