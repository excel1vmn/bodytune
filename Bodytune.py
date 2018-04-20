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

s = Server(sr=48000, nchnls=8, buffersize=1024, duplex=False)
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

lf = Sine(2, mul=15, add=20)
lf2 = LFO([.43,.41], sharp=.7, type=2, mul=1, add=1)
lf3 = LFO(freq=lf, sharp=lf2, type=7, mul=500, add=700)

#Variables globales
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
TAPS = 16
BPM = 60
BPS = Sig(60/BPM)
FLUX = SigTo(100, 0.1, 100)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Instances des instruments
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
granuleStrecth = Pad(path6, BPS, 2, 1, 5000)
granuleStrecthRumble = Pad(path6, BPS, 2, 1, FLUX, 50, FLUX*5, 0)
f1 = Pad(path16, BPS, 2, 3)
f2 = Pad(path7, BPS, 2, 2)
grosNoise = Pad(path9, BPS, 2 ,2, FLUX.value, 2000) #ajout modulation du sidechain
#g = Mangler(path12, TAPS, BPS, transp=1, segments=9, segdur=0.55, w1=100, w2=50, w3=80, poly=3, newyork=1)

#Tonale
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
douxPadGranule = ManglerExpMulti([path5,path5], TAPS, BPS, transp=0.8, segments=5, segdur=0.7, w1=100, w2=0, w3=50, poly=4, newyork=1, fFreq=5000, envTable=[(0,0),(100,1),(8100,1),(8190,0)])
douxPadGranuleAccu1 = ManglerExpMulti([path5,path5], TAPS, BPS, transp=0.8, segments=5, segdur=0.75, w1=100, w2=0, w3=0, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])
douxPadGranuleAccu2 = ManglerExpMulti([path5,path5], TAPS, BPS, transp=0.9, segments=5, segdur=0.6, w1=100, w2=0, w3=0, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])

douxPadGranulepitchMod = ManglerExpMulti([path5,path5], TAPS, BPS, transp=FLUX+0.75, segments=5, segdur=0.7, w1=100, w2=0, w3=50, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])
douxPadGranuleAccu1pitchMod = ManglerExpMulti([path5,path5], TAPS, BPS, transp=(FLUX*0.75)+0.75, segments=5, segdur=0.75, w1=100, w2=0, w3=0, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])
douxPadGranuleAccu2pitchMod = ManglerExpMulti([path5,path5], TAPS, BPS, transp=(FLUX*0.75)+0.75, segments=5, segdur=0.6, w1=100, w2=0, w3=0, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])

voxyLine = ManglerExpMulti([path7], TAPS, BPS, transp=1, segments=4, segdur=0.7, w1=100, w2=0, w3=0, poly=4, newyork=1)

granules = ManglerExpMulti([path5,path5], TAPS, BPS, transp=0.8, segments=5, segdur=0.7, w1=100, w2=0, w3=50, poly=8, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])
douxPad = Pad(path5, BPS, dns=4, transp=(FLUX*0.5)+0.75, fFreq=150, fRatio=1000)
lowPad = ManglerExpMulti([path5], TAPS, BPS, transp=0.8, segments=5, segdur=0.7, w1=100, w2=0, w3=0, poly=4, newyork=1)
stutterPad = ManglerExpMulti([path18,path19], TAPS, BPS, drive=3, transp=1.8, segments=3, segdur=0.45, w1=80, w2=50, w3=70, poly=4, newyork=1)
arpCrazy = Mangler(path4, TAPS, BPS*0.25, segments=5, segdur=0.165, w1=100, w2=20, w3=70, poly=2)
kickCrazy = Mangler(path10, TAPS, BPS, transp=2, segments=7, segdur=0.165, w1=100, w2=20, w3=70, poly=4)


granuleAccu = Drums(path9, TAPS, BPS, w1=80, w2=50, w3=60, transp=(FLUX*0.5)+0.75, sMul=8, envTable=[(0,0),(10,1),(8180,1),(8190,0)])

#Voix
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
transparent = Drums(path2, TAPS, BPS, w1=100, w2=0, w3=0, transp=(FLUX+0.25), sMul=0.125)
transparentPad = Pad(path2, BPS, dns=4, transp=(FLUX*0.5)+0.75, fFreq=FLUX, fRatio=100)
transparentGranule = ManglerExpMulti([path2], TAPS, BPS, drive=3, transp=(FLUX*0.5)+0.75, segments=3, segdur=0.02, w1=100, w2=0, w3=50, poly=2, newyork=0, fFreq=FLUX, fRatio=1000)


h1 = ManglerExp(path2, path14, TAPS, BPS, drive=0.2, segments=12, segdur=0.25, w1=100, w2=0, w3=50, poly=2)
h2 = ManglerExp(path5, path8, TAPS, BPS, drive=0.8, segments=12, segdur=0.05, w1=100, w2=0, w3=50, poly=4)
h = ManglerExp(path9, path10, TAPS, BPS, drive=0.5, segments=24, segdur=0.12, w1=100, w2=0, w3=50, poly=4)


#Percussions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
kickH = Drums(path10, TAPS, BPS, 100, 50, 30, 1, type=1)
kickL = Drums(path101, TAPS, BPS, 80, 10, 50, 0.7, freq=150, type=0)
kickLFast = Drums(path16, TAPS, BPS, 90, 10, 35, 0.5, freq=50, type=1, sMul=8)
drumCluster = ManglerExpMulti([path11,path12,path13,path14,path15], TAPS, BPS, drive=2, transp=1, segments=8, segdur=0.7, w1=20, w2=50, w3=30, poly=4, newyork=1)
drumClusterSend = ManglerExpMulti([path11,path12,path13,path14,path15], TAPS, BPS, drive=2, transp=1, segments=8, segdur=0.7, w1=100, w2=50, w3=30, poly=4, newyork=1)

#transparent = ManglerExpMulti([path2,path17,path7,path10], TAPS, BPS, drive=0.5, transp=1, segments=8, segdur=0.1, w1=100, w2=5, w3=100, poly=2, newyork=1)

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
        granuleStrecth.fade(1, 30)
        granuleStrecth.fFreq.time = 25
        granuleStrecth.fFreq.value = 50
    elif dur == 13:
        douxPadGranule.play(0, gen=False)
        douxPadGranule.fade(0.7, 10)
        douxPadGranule.fFreq.time = 10
        douxPadGranule.fFreq.value = 50
    elif dur == 39:
        granuleStrecth.fade(0, 0.1)
        douxPadGranule.fade(0, 0.1)
    elif dur == 40:
        granuleStrecth.randomize(0.8, 1.2)
        granuleStrecth.fade(0.8, 15)
        douxPadGranule.fade(0.9, 2)
    elif dur == 43:
        douxPadGranule.fade(0, 20)
    elif dur == 70:
        granuleStrecth.fade(0, 2)
        stutterPad.play(0)
        stutterPad.fade(0.5, 10)
    elif dur == 75:
        granuleStrecth.stop()
        douxPadGranule.stop()
    elif dur == 85:
        stutterPad.sideChain(1)
        grosNoise.play()
    elif dur == 90:
        grosNoise.sideChain(0.6)
    elif dur == 110:
        grosNoise.fade(0, 0.01)
        stutterPad.generate(4, 0.015)
        lowPad.play(0.6, gen=False)
    elif dur == 115:
        lowPad.fade(0, 2)
        grosNoise.stop()
    elif dur == 120:
        lowPad.fade(0.8, 3)#ajouter impacte
        stutterPad.fade(1, 7)
    elif dur == 129:
        lowPad.fade(0, 0.01)
        stutterPad.fade(0, 0.01)
    elif dur == 130:
        lowPad.stop()
        stutterPad.fade(1, 5)
    elif dur == 135:
        kickL.play(0.2)
        lowPad.play(gen=False)
        grosNoise.play()
        grosNoise.sideChain(1)
    elif dur == 139:
        stutterPad.fade(0, 0.1)
    elif dur == 140:
        stutterPad.stop()
    elif dur == 150:
        grosNoise.randomize(.1, 10)
        f2.play(0)
        f2.fade(0.8, 10)
        kickL.fade(0.6, 10)
    elif dur == 170:
        f2.randomize(0.2, 1.2)#coupure nette
        kickH.play(0)
        kickH.fade(0.8, 30)
        grosNoise.fade(1.5, 20)
    elif dur == 200:
        grosNoise.fade(0, 0.1)
        f2.stop()
        kickH.stop()
        kickL.stop()
        lowPad.fade(0.1, 1)
        douxPadGranule.play(0.2, gen=False)
        douxPadGranule.fade(0.6, 20)
        douxPadGranule.generate(2, 0.5)
        douxPadGranuleAccu1.play(0, gen=False)
        douxPadGranuleAccu2.play(0, gen=False)
        douxPadGranuleAccu1.fade(0.5, 15)
        douxPadGranuleAccu2.fade(0.5, 15)
    elif dur == 205:
        grosNoise.stop()
        lowPad.stop()
    elif dur == 230:
        douxPadGranule.generate(2, 0.5)
        douxPadGranuleAccu1.generate(2, 0.5)
        douxPadGranuleAccu2.generate(2, 0.5)
    elif dur == 250:
        douxPadGranule.fade(1, 5)
        douxPadGranuleAccu1.fade(0.8, 5)
        douxPadGranuleAccu2.fade(0.8, 5)
        stutterPad.play(0, gen=False)
    elif dur == 260:
        douxPadGranule.fade(0, 0.01)
        arpCrazy.play(0.2)
        arpCrazy.fade(0.7, 30)
        stutterPad.fade(0.8, 2)
        stutterPad.generate(11, 0.1)
    elif dur == 295:
        kickLFast.play(0)
    elif dur == 300:
        kickLFast.fade(0.2, 0.1)
        kickCrazy.play(0)
        douxPadGranule.fade(1, 5)
        douxPadGranuleAccu1.fade(1, 5)
        douxPadGranuleAccu2.fade(1, 5)
        douxPadGranule.generate(2, 0.009)
        douxPadGranuleAccu1.generate(2, 0.008)
        douxPadGranuleAccu2.generate(2, 0.009)
    elif dur == 320:
        kickCrazy.fade(0.6, 15)
        kickLFast.fade(1, 25)
        douxPadGranule.generate(2, 0.008)
        douxPadGranuleAccu1.generate(2, 0.007)
        douxPadGranuleAccu2.generate(2, 0.008)
    elif dur == 340:
        voxyLine.play(0)
        voxyLine.fade(1.2, 20)
        douxPadGranule.generate(2, 0.004)
        douxPadGranuleAccu1.generate(3, 0.009)
        douxPadGranuleAccu2.generate(3, 0.01)
        douxPadGranulepitchMod.play(0)
        douxPadGranuleAccu1pitchMod.play(0)
        douxPadGranuleAccu2pitchMod.play(0)
    elif dur == 350:
        douxPadGranulepitchMod.play(0)
        douxPadGranuleAccu1pitchMod.play(0)
        douxPadGranuleAccu2pitchMod.play(0)
        douxPadGranulepitchMod.generate(2, 0.004)
        douxPadGranuleAccu1pitchMod.generate(3, 0.009)
        douxPadGranuleAccu2pitchMod.generate(3, 0.01)
        douxPadGranulepitchMod.fade(1, 8)
        douxPadGranuleAccu1pitchMod.fade(1, 8)
        douxPadGranuleAccu2pitchMod.fade(1, 8)
        douxPadGranule.fade(0, 10)
        douxPadGranuleAccu1.fade(0, 10)
        douxPadGranuleAccu2.fade(0, 10)
        arpCrazy.fade(0, 10)
        stutterPad.fade(0, 20)
    elif dur == 365:
        kickCrazy.fade(0, 0.5)
        kickLFast.fade(0, 0.1)
    elif dur == 370:
        kickLFast.stop()
        kickCrazy.stop()
        arpCrazy.stop()
    elif dur == 380:
        stutterPad.stop()
        douxPadGranule.stop()
        douxPadGranuleAccu1.stop()
        douxPadGranuleAccu2.stop()
    elif dur == 420:
        voxyLine.fade(0, 20)
    elif dur == 450:
        voxyLine.stop()
    elif dur == 500:
        transparent.play(0)
        transparentPad.play(0)
        transparentGranule.play(0)
        transparent.fade(0.2, 10)
        transparentPad.fade(0.4, 10)
        transparentGranule.fade(0.8, 10)
    elif dur == 550:
        transparent.fade(0.8, 0.1)
        transparent.fade(0.2, 1)
        transparentPad.fade(0, 20)
        transparentGranule.fade(0, 15)
        douxPadGranulepitchMod.fade(0, 15)
        douxPadGranuleAccu1pitchMod.fade(0, 15)
        douxPadGranuleAccu2pitchMod.fade(0, 15)
    elif dur == 555:
        transparent.fade(0, 10)


def pp(address, *args):
    global FLUX, BPM
    BPM = args[1]
    FLUX.value = args[0]/1024
    #print(BPM)
    print(FLUX.value)

r = OscDataReceive(9001, "/BPM", pp)
sender = OscDataSend("iffffff", 18032, '/spat/serv')

def checkBPM():
    BPS.value = (60/BPM) + 1
    BPS.value -= 1
    FLUX.time = BPS
    globalM.time = BPS
    print(BPM)
    #print(FLUX.value)

globalM = Metro(time=BPS)
checkBPM = TrigFunc(globalM, checkBPM)
checkTime = TrigFunc(globalM, timeLine)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Gestion des outputs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
padComp = Compress(douxPad.sig()+douxPadGranule.sig()+lowPad.sig()+stutterPad.sig()+douxPadGranulepitchMod.sig(), thresh=-24, ratio=6, risetime=.01, falltime=.2, knee=0.5)

padMix = Mix(padComp, mul=0.4).out(0)

percMix = Mix(kickH.sig()+kickL.sig()+granules.sig()+kickCrazy.sig()+kickLFast.sig(), mul=0.4).out(1)

sparkMix = Mix(arpCrazy.sig()+voxyLine.sig()).out(2)

preClip = Clip(grosNoise.sig(), max=1.4, mul=0.8)
noiseMix = Mix(fat.sig()+granuleStrecth.sig()+granuleStrecthRumble.sig()+preClip+f1.sig()+f2.sig()+h.sig()+h1.sig()+h2.sig()+drumCluster.sig()+granuleAccu.sig(), mul=0.2).out(3)

spatLMix = Mix(douxPadGranuleAccu1.sig()+douxPadGranuleAccu1pitchMod.sig(), mul=0.3).out(4)
spatRMix = Mix(douxPadGranuleAccu2.sig()+douxPadGranuleAccu2pitchMod.sig(), mul=0.3).out(5)

voxMix = Mix(transparent.sig()+transparentPad.sig()+transparentGranule.sig(), mul=0.2).out(6)

subSplit = EQ(padComp+padMix+sparkMix+noiseMix+spatLMix+spatRMix+voxMix, freq=80, q=1, type=1, mul=0.1)
subMix = Mix(subSplit, mul=0.1).out(7)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#p1 = Phasor(freq=0.01, mul=pi, add=0)

'''
1. (i) The source number starting at 0.
2. (f) The azimuth value between 0 and pi*2.
3. (f) The elevation value between 0 and pi.
- 0 = top vertex of the dome.
- pi/2 = center of the sphere (the height of the lower circle of a half-sphere). - pi = lower vertex of the dome (under the floor).
4. (f) The span in azimuth between 0 and 2.
5. (f) The span in elevation between 0 and 0.5.
'''
msg = [0, 0, pi/2.5, 0.5, .12, 0, 0]
sender.send(msg)
msg = [1, 0, pi/2, 1, 0, 0, 0]
sender.send(msg)
msg = [2, 0, pi/2, 1, .5, 0, 0]
sender.send(msg)
msg = [3, 0, pi/2, 1, 0, 0, 0]
sender.send(msg)
msg = [4, pi*1.75, pi/2, 0.5, 0.5, 0, 0]
sender.send(msg)
msg = [5, pi/4, pi/2, 0.5, 0.5, 0, 0]
sender.send(msg)
msg = [6, 0, pi/2, 1, 0, 0, 0]
sender.send(msg)

#s.start()
s.gui(locals())
