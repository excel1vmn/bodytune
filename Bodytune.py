#!/usr/bin/env python3
# encoding: utf-8
from pyo import *
from inst.granl import *
#from seqs.s1 import *

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

def pp(address, *args):
    print(address)
    print(args)

r = OscDataReceive(9001, "/PS", pp)

"""
def checkBPM():
    globalM.time = 60 / bpm

bpm = 90
globalM = Metro(time=60/90).play()
globalC = Counter(globalM, min=0, max=10000, dir=0, mul=1)
check = TrigFunc(globalM, checkBPM)
"""

TAPS = 16

path = 'sndsSB/plus.aif'
path2 = 'sndsSB/synthStaccato.aif'

a = Granl(path,[0.5,1,2,4,8,16],2,0.5,1.2,150,1,120,1)
b = Granl(path2,[0.9,1,1.1],10,0.99,1.01,20,1,40,2)

rev = Freeverb(a.sig()+b.sig(), size=0.50, damp=0.50, bal=0.20, mul=0.2).out()

s.gui(locals())
