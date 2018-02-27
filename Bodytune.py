#!/usr/bin/env python3
# encoding: utf-8
from pyo import *
from inst.granl import *
from inst.drums import *
from inst.pad import *
from inst.mangler import *
from inst.manglerexp import *
from inst.manglerexpmulti import *
from inst.fattener import *
import math

s = Server(sr=48000, nchnls=2, buffersize=512, duplex=False).boot()

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
path101 = 'sndsKick/crossbreed_forReal_4sidechain_15.wav'
path11 = 'sndsDrums/103-67_1_break.wav'
path12 = 'sndsDrums/104-05_2_bars_f-c_open_hats.wav'
path13 = 'sndsDrums/100-05_3_bar_crashes_break.wav'
path14 = 'sndsDrums/118-52_1_2_bar_tom_snr_fill.wav'
path15 = 'sndsDrums/125-37_2_bar_linear_groove.wav'
path16 = 'sndsSB/boaing.wav'
path17 = 'snds/baseballmajeur_s.aif'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Variables globales
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
TAPS = 16
BPM = 60
BPS = 60/BPM
TM = BPS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Instances des instruments
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


sine = SineLoop(freq=[49,50,51], mul=0.2)
sf = SfPlayer(path9, loop=True).play()

d = Drums(path10, TAPS, BPS, 100, 50, 30, 1, 1)
e = Drums(path101, TAPS, BPS, 80, 10, 50, 0.5, 0)
f = Pad(path6, 2, 1)
f1 = Pad(path16, 2, 3)
f2 = Pad(path7, 2, 2)
f3 = Pad(path9, 2 ,2)
#g = Mangler(path12, TAPS, TM, transp=1, segments=9, segdur=0.55, w1=100, w2=50, w3=80, poly=3, newyork=1)
#h = ManglerExp(path2, path14, TAPS, TM, drive=0.2, segments=12, segdur=0.25, w1=100, w2=0, w3=50, poly=2)
#h = ManglerExp(path2, path8, TAPS, TM, drive=0.5, segments=TAPS, segdur=0.12, w1=100, w2=0, w3=50, poly=4)
h = ManglerExp(path9, path10, TAPS, TM, drive=0.5, segments=24, segdur=0.12, w1=100, w2=0, w3=50, poly=4)
i = ManglerExpMulti([path11,path12,path13,path14,path15], TAPS, TM, drive=2, transp=1, segments=8, segdur=0.7, w1=20, w2=50, w3=30, poly=4, newyork=1)
i1 = ManglerExpMulti([path11,path12,path13,path14,path15], TAPS, TM, drive=2, transp=1, segments=8, segdur=0.7, w1=20, w2=50, w3=30, poly=4, newyork=1)
j = ManglerExpMulti([path2,path17,path7,path10], TAPS, TM, drive=0.5, transp=1, segments=6, segdur=TM, w1=100, w2=5, w3=3, poly=2, newyork=1)

a = Fattener(i1.sig(), BPS, 3)

'''[path2,path17,path7,path10]'''

'''
c = []
for clist in range(3):
    clist+1
    c.append(Pad(path3,1, 0.1*clist))
    #c[i-1].play(0.3)
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Gestion du TEMPS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
dur = 0
def timeLine():
    global dur
    print(dur)
    dur += 1
    if dur == 1:
        f.play()
        f.fadeIn(1, 15)
    elif dur == 14:
        f.fadeOut(0, 0.2, 0.2)
    elif dur == 15:
        f.randomize(0.75, 1.25)
        f.fadeIn(0.8, 20)
        a.play()
        a.fadeIn(0.8, 20)
    elif dur == 20:
        i.play()
        i.fadeIn(1.2, 0.01)
        e.play(0.2)
        e.fadeOut(0, 0.2, 0.2)
    elif dur == 24:
        e.stop()
        d.play(0.2)
        d.fadeOut(0, 0.2, 0.2)
        f.randomize(0.99, 1.01)
    elif dur == 25:
        d.stop()
        i.invState()
        f1.play()
        f1.fadeIn(0.8, 10)
    elif dur == 40:
        i.stop()
        e.play(0.2)
    elif dur == 50:
        e.stop()
        i1.play(1.2)
        a.play()
        f.fadeOut(0.5, 2)
        f1.stop()
        f2.play()
        f2.fadeIn(0.8,0.2)
        f2.sideChain(1, BPS)

def pp(address, args):
    print(address)
    print(args)
    BPM = args[1]

r = OscDataReceive(9001, ["/FEED","/BPM"], pp)

def checkBPM():
    globalM.time = 60 / BPM
    BPS = 60 / BPM

globalM = Metro(time=BPS).play()
checkBPM = TrigFunc(globalM, checkBPM)
checkTime = TrigFunc(globalM, timeLine)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Gestion des outputs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
mix = Pan(a.sig()+d.sig()+e.sig()+f.sig()+f1.sig()+f2.sig()+f3.sig()+h.sig()+j.sig(), mul=1)
clip = Clip(mix, min=-1.00, max=1.00, mul=0.5).out()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#s.start()
s.gui(locals())
