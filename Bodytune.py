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

s = Server(sr=48000, nchnls=12, buffersize=512, duplex=False)
s.setOutputDevice(2)
s.boot()
pa_list_devices()

#Liste de chemin vers divers son dans un dossier inclu dans l'architecture
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
path1 = 'sndsSB/plus.aif'
path2 = 'snds/transparent.aif'
path3 = 'sndsSB/synthSqueal.aif'
path4 = 'sndsSB/Znfast.aif'
path5 = 'sndsSB/resonPad.wav'
path6 = 'sndsSB/synthStutter.aif'
path7 = 'snds/voxyline.aif'
path8 = 'snds/epic.aif'
path9 = 'sndsSB/Xprime.aif'
path10 = 'sndsKick/crossbreed_forReal_4sidechain_10.wav'
path101 = 'sndsKick/crossbreed_forReal_4sidechain_15.wav'
path11 = 'sndsDrums/103-67_1_break.wav'
path12 = 'sndsDrums/104-05_2_bars_f-c_open_hats.wav'
path13 = 'sndsDrums/100-05_3_bar_crashes_break.wav'
path14 = 'sndsDrums/118-52_1_2_bar_tom_snr_fill.wav'
path15 = 'sndsDrums/125-37_2_bar_linear_groove.wav'
path16 = 'sndsSB/boaing.wav'
path17 = 'snds/baseballmajeur_s.aif'
path18 = 'sndsSB/padStutter.aif'
path19 = 'sndsSB/Nprime.aif'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Variables globales
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
TAPS = 16
BPM = 85
BPS = Sig(60/BPM)
BFLUX = SigTo(1, BPM/60)
FLUX = SigTo(500, 1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Instances des instruments
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


sine = SineLoop(freq=[49,50,51], mul=0.2)
sf = SfPlayer(path9, loop=True).play()

kickH = Drums(path10, TAPS, BPS, 100, 50, 30, 1, type=1)
kickL = Drums(path101, TAPS, BPS, 80, 10, 50, 0.6, freq=100, type=0)
granuleStrecth = Pad(path6, BPS, 2, 1)
f1 = Pad(path16, BPS, 2, 3)
f2 = Pad(path7, BPS, 2, 2)
grosNoise = Pad(path9, BPS, 2 ,2)
#g = Mangler(path12, TAPS, BPS, transp=1, segments=9, segdur=0.55, w1=100, w2=50, w3=80, poly=3, newyork=1)

#Tonale
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
douxPad = Mangler(path5, TAPS, BPS, transp=0.7, segments=5, segdur=0.7, w1=100, w2=0, w3=0, poly=4, newyork=1)
lowPad = Mangler(path5, TAPS, BPS, transp=0.2, segments=5, segdur=0.7, w1=100, w2=0, w3=0, poly=4, newyork=1)
stutterPad = ManglerExpMulti([path18,path19], TAPS, BPS, drive=3, transp=1.8, segments=3, segdur=0.45, w1=80, w2=50, w3=70, poly=4, newyork=1)
arpCrazy = Mangler(path4, TAPS, BPS*0.25, segments=5, segdur=0.165, w1=100, w2=20, w3=70, poly=2)


granuleAccu = Drums(path9, TAPS, BPS, w1=80, w2=50, w3=60, transp=FLUX, sMul=8)


h1 = ManglerExp(path2, path14, TAPS, BPS, drive=0.2, segments=12, segdur=0.25, w1=100, w2=0, w3=50, poly=2)
h2 = ManglerExp(path5, path8, TAPS, BPS, drive=0.8, segments=12, segdur=0.05, w1=100, w2=0, w3=50, poly=4)
h = ManglerExp(path9, path10, TAPS, BPS, drive=0.5, segments=24, segdur=0.12, w1=100, w2=0, w3=50, poly=4)

#Percussions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
drumCluster = ManglerExpMulti([path11,path12,path13,path14,path15], TAPS, BPS, drive=2, transp=1, segments=8, segdur=0.7, w1=20, w2=50, w3=30, poly=4, newyork=1)
drumClusterSend = ManglerExpMulti([path11,path12,path13,path14,path15], TAPS, BPS, drive=2, transp=1, segments=8, segdur=0.7, w1=100, w2=50, w3=30, poly=4, newyork=1)

transparent = ManglerExpMulti([path2,path17,path7,path10], TAPS, BPS, drive=0.5, transp=1, segments=8, segdur=0.1, w1=100, w2=5, w3=100, poly=2, newyork=1)

fat = Fattener(drumClusterSend.sig(), BPS, 5)

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
        granuleStrecth.play(0)
        granuleStrecth.fadeIn(1, 40)
    elif dur == 13:
        douxPad.play(0)
        douxPad.fadeIn(0.5, 30)
    elif dur == 39:
        granuleStrecth.fadeOut(0, 0.2, 0.2)
        douxPad.fadeOut(0, 0.2, 0.2)
    elif dur == 40:
        granuleStrecth.randomize(0.8, 1.2)
        granuleStrecth.fadeIn(0.8, 30)
        douxPad.fadeIn(0.9, 3)
    elif dur == 43:
        douxPad.fadeOut(0.2, 25)
    elif dur == 70:
        granuleStrecth.fadeOut(0, 2, 0.75)
        stutterPad.play(0)
        stutterPad.fadeIn(0.7,1)
    elif dur == 75:
        granuleStrecth.stop()
    elif dur == 85:
        stutterPad.sideChain(1)
        grosNoise.play(0.6)
    elif dur == 90:
        grosNoise.sideChain(1)

    '''
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
    elif dur == 52:
        f.stop()
        f2.sideChain(1, BPS)
    elif dur == 100:
        f1.play()
        f1.fadeIn(1,10)
    '''



def pp(address, args):
    global BPM
    print(address)
    print(args)
    FLUX = args[0]
    BPM = args[1]

r = OscDataReceive(9001, ["/FEED","/BPM"], pp)
sender = OscDataSend("iffffff", 18032, '/spat/serv')

#sender.send()

def checkBPM():
    BPS.value = 60/BPM
    globalM.time = BPS

globalM = Metro(time=BPS).play()
checkBPM = TrigFunc(globalM, checkBPM)
checkTime = TrigFunc(globalM, timeLine)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Gestion des outputs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
mix = Mix(fat.sig()+kickH.sig()+kickL.sig()+granuleStrecth.sig()+f1.sig()+f2.sig()+arpCrazy.sig()+grosNoise.sig()+h.sig()+h1.sig()+h2.sig()+drumCluster.sig()+transparent.sig()+douxPad.sig()+stutterPad.sig()+granuleAccu.sig(), mul=0.2).mix(2).out()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#s.start()
s.gui(locals())
