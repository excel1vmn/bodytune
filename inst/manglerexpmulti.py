from pyo import *
import random

class ManglerExpMulti:
    def __init__(self, paths, TAPS, TM, drive=1, transp=1, segments=8, segdur=0.125, w1=100, w2=0, w3=0, poly=1, newyork=0, fFreq=2000, fRatio=2000, envTable=[(0,0),(32,1),(8100,1),(8190,0)]):
        self.dur = []
        self.paths = paths
        self.tm = TM
        self.taps = TAPS
        self.pitch = transp
        self.segments = segments
        self.segdur = segdur
        self.fFreq = fFreq
        if fFreq <= 1:
            self.fFreq = (fFreq * fRatio) + 50
        self.isOn = 0
        for i in range(len(self.paths)):
            self.dur.append(sndinfo(self.paths[i])[1])

        self.env = CosTable(envTable)
        self.whatTab = 0
        self.tab = [SndTable(initchnls=2), SndTable(initchnls=2)]
        self.beat = Beat(self.tm, self.taps, w1, w2, w3, poly).play()
        self.transp = self.tab[self.whatTab].getRate()
        '''
        self.amp = OscTrig(self.env, self.beat, self.tab.getRate())
        self.osc = OscTrig(self.tab, self.beat, self.tab.getRate(), interp=4, mul=2)
        '''
        self.crossFade1 = SigTo(0, time=0.1)
        self.crossFade2 = SigTo(0, time=0.1)
        self.amp1 = OscTrig(self.env, self.beat, self.tab[self.whatTab].getRate()*transp)
        self.osc1 = OscTrig(self.tab[self.whatTab], self.beat, self.tab[self.whatTab].getRate()*transp, interp=4, mul=self.crossFade1)
        self.amp2 = OscTrig(self.env, self.beat, self.tab[self.whatTab].getRate()*transp)
        self.osc2 = OscTrig(self.tab[self.whatTab], self.beat, self.tab[self.whatTab].getRate()*transp, interp=4, mul=self.crossFade2)
        self.fol = Follower(self.osc1+self.osc2, freq=20)
        self.dist = Disto(self.osc1+self.osc2, drive=drive*self.fol, slope=2)
        self.filt = Biquad(self.osc1+self.osc2, 30+self.fol*40, q=2, type=1)
        self.bp = ButBP(self.dist, freq=self.fFreq, q=4)
        self.lp = Biquad(self.bp, freq=1000, q=2, type=0, mul=newyork)
        self.comp = Compress(self.filt+self.lp, thresh=-30, ratio=8, risetime=.01, falltime=.2, knee=0.2)
        self.panMul = SigTo(0)
        self.panPow = Pow(self.panMul, 3)
        self.pan = Pan(self.comp, outs=2, mul=self.panPow)

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
        self.amp1.play()
        self.osc1.play()
        self.amp2.play()
        self.osc2.play()
        self.fol.play()
        self.dist.play()
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
        self.amp1.stop()
        self.osc1.stop()
        self.amp2.stop()
        self.osc2.stop()
        self.fol.stop()
        self.dist.stop()
        self.filt.stop()
        self.bp.stop()
        self.lp.stop()
        self.panMul.stop()
        self.panPow.stop()
        self.pan.stop()
        self.end.stop()

    def fade(self, value, time):
        self.panMul.time = time
        self.panMul.value = value

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
        if self.whatTab == 0:
            self.crossFade1.value = 1
            self.crossFade2.value = 0
        else:
            self.crossFade2.value = 1
            self.crossFade1.value = 0
        start = random.uniform(0, self.dur[0]-segdur-0.5)
        stop = start + segdur
        self.tab[self.whatTab].setSound(self.paths[0], start, stop)
        for l in range(segments-1):
            if l >= len(self.dur):
                l = 0
            else:
                start = random.uniform(0, self.dur[l]-segdur-0.5)
                stop = start + segdur
                self.tab[self.whatTab].append(self.paths[l], 0.5, start, stop)
                l += 1

        newfreq = 1 / (segments * segdur)
        if self.whatTab == 0:
            self.amp1.freq = (newfreq * self.transp) * self.pitch
            self.osc1.freq = (newfreq * self.transp) * self.pitch
            self.whatTab = 1
        else:
            self.amp2.freq = (newfreq * self.transp) * self.pitch
            self.osc2.freq = (newfreq * self.transp) * self.pitch
            self.whatTab = 0
        self.end.time = 1 / (newfreq * (self.transp * self.pitch))
