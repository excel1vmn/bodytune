from pyo import *
import random

class ManglerExpMulti:
    def __init__(self, paths, TAPS, TM, panval=0.5, drive=1, transp=1, segments=8, segdur=0.125, w1=100, w2=0, w3=0, poly=1, newyork=0):
        self.dur = []
        self.paths = paths
        self.pitch = transp
        for i in range(len(self.paths)):
            self.dur.append(sndinfo(self.paths[i])[1])
            '''
            print(self.paths[i])
            print(len(self.dur))
            print(self.dur)
            '''
             
        self.env = CosTable([(0,0),(32,1),(8100,1),(8191,0)])
        self.tab = SndTable(initchnls=2)
        self.beat = Beat(TM, TAPS, w1, w2, w3, poly)
        self.transp = self.tab.getRate()
        self.amp = OscTrig(self.env, self.beat, self.tab.getRate())
        self.osc = OscTrig(self.tab, self.beat, self.tab.getRate(), interp=4, mul=2)
        self.fol = Follower(self.osc, freq=20)
        self.dist = Disto(self.osc, drive=drive*self.fol, slope=2)
        self.filt = Biquadx(self.osc, 30+self.fol*40, q=2, type=1)
        self.bp = Biquadx(self.dist, freq=2000, q=4, type=2, stages=6)
        self.lp = Biquadx(self.bp, freq=1000, q=2, type=0, stages=6, mul=newyork)
        self.comp = Compress(self.filt+self.lp, thresh=-30, ratio=8, risetime=.01, falltime=.2, knee=0.2)
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
        start = random.uniform(0, self.dur[0]-segdur-0.002)
        stop = start + segdur
        self.tab.setSound(self.paths[0], start, stop)
        for l in range(segments-1):
            if l >= len(self.dur):
                l = 0
            else:
                start = random.uniform(0, self.dur[l]-segdur-0.002)
                stop = start + segdur
                self.tab.append(self.paths[l], 0.002, start, stop)
                l += 1
                   
        newfreq = 1 / (segments * segdur)
        self.amp.freq = (newfreq * self.transp) * self.pitch
        self.osc.freq = (newfreq * self.transp) * self.pitch
        self.end.time = 1 / (newfreq * (self.transp * self.pitch))