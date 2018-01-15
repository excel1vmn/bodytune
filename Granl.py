from pyo import *
import random

s = Server().boot()

class Granl:
    def __init__(self, path):
        self.env = HannTable()
        self.snd = SndTable(path)
        self.pos = Phasor(self.snd.getRate()*.25, 0, self.snd.getSize())
        self.dur = Noise(.001, .1)
        self.g = Granulator(self.snd, self.env, 1, self.pos, self.dur, grains=8, basedur=0.10)
        self.pan = Pan(self.g, outs=2, pan=0.50, spread=0.50, mul=1, add=0)
        
    def out(self):
        self.pan.out()
        return self
        
    def sig(self):
        return self.pan


path = 'snds/epic.aif'

a = Granl(path)

v = Freeverb(a.sig(), size=0.50, damp=0.50, bal=0.50, mul=1, add=0).out()

s.gui(locals())