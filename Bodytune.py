#!/usr/bin/env python3
# encoding: utf-8
from pyo import *
from inst.granl import *
from inst.drums import *
from inst.pad import *
from inst.mangler import *
from inst.manglerexp import *
from inst.manglerexpmulti import *
import math

s = Server(duplex=False).boot()

#Variables globales
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
TM = .5625
TAPS = 16
BPM = 130
BPS = 60/BPM
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def pp(address, args):
    print(address)
    print(args)
    BPM = args[1]

r = OscDataReceive(9001, ["/FEED","/BPM"], pp)

def checkBPM():
    globalM.time = 60 / BPM
    BPS = 60 / BPM

globalM = Metro(time=BPS).play()
globalC = Counter(globalM, min=0, max=10000, dir=0, mul=1)
check = TrigFunc(globalM, checkBPM)

#Liste de chemin vers divers son dans un dossier inclu dans l'architecture
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
path1 = 'sndsSB/plus.aif'
path2 = 'snds/transparent.aif'
path3 = 'sndsSB/synthSqueal.aif'
path4 = 'snds/kick.aif'
path5 = 'sndsSB/resonPad.wav'
path6 = 'sndsSB/synthStutter.aif'
path7 = 'snds/voxyline.aif'
path8 = 'snds/epic.aif'
path9 = 'snds/wubarp.aif'
path10 = 'sndsKick/crossbreed_forReal_4sidechain_10.wav'
path11 = 'sndsDrums/103-67_1_break.wav'
path12 = 'sndsDrums/104-05_2_bars_f-c_open_hats.wav'
path13 = 'sndsDrums/100-05_3_bar_crashes_break.wav'
path14 = 'sndsDrums/118-52_1_2_bar_tom_snr_fill.wav'
path15 = 'sndsDrums/125-37_2_bar_linear_groove.wav'
path16 = 'sndsSB/boaing.wav'
path17 = 'snds/baseballmajeur_s.aif'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Instances des instruments
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
a = Granl(path4,[0.5,1,2,4],2,0.5,1.2,15,1,120,1)
'''
b = Granl(path2,[0.9,1,1.1],10,0.99,1.01,5,1,40,2)
c = []
d = Drums(path10, TAPS, BPS, 100, 50, 30, 1, 1)
e = Drums(path1, TAPS, BPS, 20, 10, 50, 4, 0)
'''
f = Pad(path6, 2, 1)
g = Mangler(path12, TAPS, TM, transp=1, segments=9, segdur=0.55, w1=100, w2=50, w3=80, poly=3, newyork=1)
#h = ManglerExp(path2, path14, TAPS, TM, drive=0.2, segments=12, segdur=0.25, w1=100, w2=0, w3=50, poly=2)
#h = ManglerExp(path2, path8, TAPS, TM, drive=0.5, segments=TAPS, segdur=0.12, w1=100, w2=0, w3=50, poly=4)
h = ManglerExp(path9, path10, TAPS, TM, drive=0.5, segments=24, segdur=0.12, w1=100, w2=0, w3=50, poly=4)
i = ManglerExpMulti([path11,path12,path13,path14,path15], TAPS, TM, drive=2, transp=1, segments=8,
                    segdur=0.7, w1=20, w2=50, w3=30, poly=4, newyork=1)
j = ManglerExpMulti([path2,path17,path9,path8], TAPS, TM, drive=0.5, transp=2, segments=TAPS,
                    segdur=TM/TAPS, w1=70, w2=50, w3=30, poly=4, newyork=1)

i.play()
'''
for i in range(3):
    i+1
    c.append(Pad(path3,1, 0.1*i))
    #c[i-1].play(0.3)
'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def allPlay():
    a.play()
    b.play()
    for i in range(len(c)):
        i+1
        c[i-1].play(0.3)
    d.play()
    f.play()
    g.play()

def allStop():
    a.stop()
    b.stop()
    c.stop()
    d.stop()
    f.stop()
    g.stop()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#Gestion des outputs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
mix = Pan(a.sig()+f.sig()+g.sig()+h.sig()+i.sig()+j.sig(), mul=1)
clip = Clip(mix, min=-1.00, max=1.00, mul=0.8).out()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#s.start()
s.gui(locals())
