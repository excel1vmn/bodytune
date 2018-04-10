from pyo import *
import random

class ManglerExpMulti:
    def __init__(self, paths, TAPS, TM, panval=0.5, drive=1, transp=1, segments=8, segdur=0.125, w1=100, w2=0, w3=0, poly=1, newyork=0, envTable=[(0,0),(32,1),(8100,1),(8190,0)]):
        self.dur = []
        self.paths = paths
        self.tm = TM
        self.taps = TAPS
        self.pitch = transp
        self.segments = segments
        self.segdur = segdur
        self.isOn = 0
        for i in range(len(self.paths)):
            self.dur.append(sndinfo(self.paths[i])[1])

        self.env = CosTable(envTable)
        self.tab = SndTable(initchnls=2)
        self.beat = Beat(self.tm, self.taps, w1, w2, w3, poly).play()
        self.transp = self.tab.getRate()
        self.amp = OscTrig(self.env, self.beat, self.tab.getRate())
        self.osc = OscTrig(self.tab, self.beat, self.tab.getRate(), interp=4, mul=2)
        self.fol = Follower(self.osc, freq=20)
        self.dist = Disto(self.osc, drive=drive*self.fol, slope=2)
        self.filt = Biquad(self.osc, 30+self.fol*40, q=2, type=1)
        self.bp = ButBP(self.dist, freq=2000, q=4)
        self.lp = Biquad(self.bp, freq=1000, q=2, type=0, mul=newyork)
        self.comp = Compress(self.filt+self.lp, thresh=-30, ratio=8, risetime=.01, falltime=.2, knee=0.2)
        self.panMul = SigTo(0)
        self.panPow = Pow(self.panMul, 3)
        self.pan = Pan(self.comp, outs=2, pan=panval, mul=self.panPow)

        self.count = 0
        self.end = TrigFunc(self.beat, self.check).stop()
        self.generate(self.segments, self.segdur)
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
        self.bp.play()
        self.lp.play()
        self.comp.play()
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
        self.bp.stop()
        self.lp.stop()
        self.comp.stop()
        self.panMul.stop()
        self.panPow.stop()
        self.pan.stop()
        self.end.stop()

    def fadeIn(self, value, time):
        self.panMul.time = time
        self.panMul.value = value

    def fadeOut(self, value, time, init=0.8):
        self.pan.mul = SigTo(value, time, init)

    def sideChain(self, str=1, dur=0.2):
        self.mTrig = Metro(time=self.tm).play()
        self.tEnv = TrigEnv(self.mTrig, self.env)
        self.clip = Clip(self.tEnv, self.pan.mul-str, 1)
        self.pan.mul = self.clip

    def new(self):
        self.wantsnew = True

    def check(self):
        if self.count == 3:
            self.generate(self.segments, self.segdur)
        else:
            self.count += 1

    def invState(self):
        if(self.isOn == 0):
            self.beat.stop()
            self.isOn = 1
        else:
            self.beat.play()
            self.isOn = 0

    def generate(self, segments, segdur):
        start = random.uniform(0, self.dur[0]-segdur-0.01)
        stop = start + segdur
        self.tab.setSound(self.paths[0], start, stop)
        for l in range(segments-1):
            if l >= len(self.dur):
                l = 0
            else:
                start = random.uniform(0, self.dur[l]-segdur-0.01)
                stop = start + segdur
                self.tab.append(self.paths[l], 0.01, start, stop)
                l += 1

        newfreq = 1 / (segments * segdur)
        self.amp.freq = (newfreq * self.transp) * self.pitch
        self.osc.freq = (newfreq * self.transp) * self.pitch
        self.end.time = 1 / (newfreq * (self.transp * self.pitch))

    def updateBPM(self, BPS):
        self.tm = BPS
