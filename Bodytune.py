#!/usr/bin/env python3
# encoding: utf-8
from pyo import *
from inst.drums import *
from inst.pad import *
from inst.mangler import *
from inst.manglerexpmulti import *
import math

s = Server(sr=48000, nchnls=9, buffersize=1024, duplex=False)
s.setOutputDevice(2)
s.boot()
s.amp = .18
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
FLUX = SigTo(100, 0.1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Instances des instruments
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
granuleStrecth = Pad(path6, BPS, 2, 1, 5000)
f2 = Pad(path7, BPS, 2, 2)
grosNoise = Pad(path9, BPS, 2 ,2, 300) #ajout modulation du sidechain
grosNoisePad = Pad(path9, BPS, 4, FLUX*0.5, 150)
grosNoiseTop = Pad(path9, BPS, 2 ,2, 500)

#Tonale
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
douxPadGranule = ManglerExpMulti([path5,path5], TAPS, BPS, transp=0.8, segments=5, segdur=0.7, w1=100, w2=0, w3=50, poly=4, newyork=1, fFreq=5000, envTable=[(0,0),(100,1),(8100,1),(8190,0)])
douxPadGranuleAccu1 = ManglerExpMulti([path5,path5], TAPS, BPS, transp=0.8, segments=5, segdur=0.75, w1=100, w2=0, w3=0, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])
douxPadGranuleAccu2 = ManglerExpMulti([path5,path5], TAPS, BPS, transp=0.9, segments=5, segdur=0.6, w1=100, w2=0, w3=0, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])

douxPadGranulepitchMod = ManglerExpMulti([path5,path5], TAPS, BPS, transp=FLUX+0.75, segments=5, segdur=0.7, w1=100, w2=0, w3=50, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])
douxPadGranuleAccu1pitchMod = ManglerExpMulti([path5,path5], TAPS, BPS, transp=(FLUX*0.75)+0.75, segments=5, segdur=0.75, w1=100, w2=0, w3=0, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])
douxPadGranuleAccu2pitchMod = ManglerExpMulti([path5,path5], TAPS, BPS, transp=(FLUX*0.75)+0.75, segments=5, segdur=0.6, w1=100, w2=0, w3=0, poly=4, newyork=1, envTable=[(0,0),(100,1),(8100,1),(8190,0)])

voxyLine = ManglerExpMulti([path7], TAPS, BPS, transp=1.8, segments=4, segdur=0.7, w1=100, w2=0, w3=0, poly=4, newyork=0, fFreq=3000)

granules = ManglerExpMulti([path18,path6], TAPS, BPS, transp=1, segments=3, segdur=0.07, w1=100, w2=0, w3=50, poly=8, newyork=0)
douxPad = Pad(path5, BPS, dns=4, transp=(FLUX*0.5)+0.75, fFreq=150, fRatio=1000)
lowPad = ManglerExpMulti([path5], TAPS, BPS, transp=0.8, segments=5, segdur=0.7, w1=100, w2=0, w3=0, poly=4, newyork=1, fFreq=200)
stutterPadL = ManglerExpMulti([path18,path19], TAPS, BPS, drive=2, transp=1.8, segments=5, segdur=0.65, w1=80, w2=50, w3=70, poly=4, newyork=0, fFreq=600)
stutterPadR = ManglerExpMulti([path18,path19], TAPS, BPS, drive=2, transp=1.8, segments=5, segdur=0.6, w1=80, w2=50, w3=70, poly=4, newyork=0, fFreq=600)

arpCrazy = Mangler(path4, TAPS, BPS*0.25, segments=5, segdur=0.165, w1=100, w2=20, w3=70, poly=2)
kickCrazy = Mangler(path10, TAPS, BPS, transp=2, segments=7, segdur=0.165, w1=100, w2=20, w3=70, poly=4)


granuleAccu = Drums(path9, TAPS, BPS, w1=80, w2=50, w3=60, transp=FLUX*4, sMul=8)

#Voix
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
transparent = Drums(path2, TAPS, BPS, w1=100, w2=0, w3=0, transp=(FLUX+0.25), sMul=0.125)
transparentPad = Pad(path2, BPS, dns=4, transp=(FLUX*0.5)+0.75, fFreq=FLUX, fRatio=100)
transparentGranule = ManglerExpMulti([path2], TAPS, BPS, drive=3, transp=(FLUX*0.5)+0.75, segments=3, segdur=0.02, w1=100, w2=0, w3=50, poly=2, newyork=0, fFreq=FLUX, fRatio=1000)

'''
h1 = ManglerExp(path2, path14, TAPS, BPS, drive=0.2, segments=12, segdur=0.25, w1=100, w2=0, w3=50, poly=2)
h2 = ManglerExp(path5, path8, TAPS, BPS, drive=0.8, segments=12, segdur=0.05, w1=100, w2=0, w3=50, poly=4)
h = ManglerExp(path9, path10, TAPS, BPS, drive=0.5, segments=24, segdur=0.12, w1=100, w2=0, w3=50, poly=4)
'''


#Percussions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
kickH = Drums(path10, TAPS, BPS, 100, 50, 30, 1, type=1)
kickL = Drums(path101, TAPS, BPS, 80, 10, 50, 0.7, freq=150, type=0)
kickLFast = Drums(path16, TAPS, BPS, 90, 10, 35, 0.5, freq=50, type=1, sMul=8)

#transparent = ManglerExpMulti([path2,path17,path7,path10], TAPS, BPS, drive=0.5, transp=1, segments=8, segdur=0.1, w1=100, w2=5, w3=100, poly=2, newyork=1)

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
        granuleStrecth.fade(1, 20)
        granuleStrecth.fFreq.time = 25
        granuleStrecth.fFreq.value = 50
    elif dur == 13:
        douxPadGranule.play(0, gen=False)
        douxPadGranule.fade(0.7, 15)
        douxPadGranule.fFreq.time = 15
        douxPadGranule.fFreq.value = 50
    elif dur == 39:
        granuleStrecth.fade(0, 0.1)
        douxPadGranule.fade(0, 0.1)
    elif dur == 40:
        granuleStrecth.fade(0, 0.1)
        douxPadGranule.fade(0, 0.1)
        granuleStrecth.randomize(0.8, 1.2)
        granuleStrecth.fade(1, 10)
        douxPadGranule.fade(0.9, 8)
    elif dur == 45:
        douxPadGranule.fade(0, 5)
    elif dur == 55:
        douxPadGranule.generate(7, 0.09)
        douxPadGranule.fade(0.8, 10)
        stutterPadL.play(0, gen=False)
        stutterPadL.fade(1, 5)
        stutterPadR.play(0, gen=False)
        stutterPadR.fade(1, 5)
    elif dur == 70:
        granuleAccu.play()
        granuleStrecth.fade(0, 5)
    elif dur == 74:
        douxPadGranule.fade(0, 15)
        grosNoisePad.play(0)
        grosNoisePad.fade(1, 20)
    elif dur == 75:
        granuleStrecth.stop()
    elif dur == 85:
        grosNoise.play(1)
    elif dur == 90:
        grosNoise.sideChain(0.6)
        douxPadGranule.stop()
    elif dur == 110:
        granuleAccu.fade(0, 0.01)
        grosNoise.fade(0, 0.01)
        stutterPadL.fade(0.7, 0.01)
        stutterPadR.fade(0.7, 0.01)
        stutterPadL.generate(4, 0.015)
        stutterPadR.generate(3, 0.015)
        lowPad.play(0.7, gen=False)
    elif dur == 115:
        lowPad.fade(0, 2)
        grosNoise.stop()
    elif dur == 120:
        lowPad.fade(0.8, 3)#ajouter impacte
        granuleAccu.fade(1, 20)
        stutterPadL.fade(1, 7)
        stutterPadL.drive.time = 5
        stutterPadL.drive.value = 20
        stutterPadR.fade(1, 7)
        stutterPadR.drive.time = 5
        stutterPadR.drive.value = 20
    elif dur == 129:
        lowPad.fade(0, 0.01)
        stutterPadL.fade(0.5, 0.1)
        stutterPadR.fade(0.5, 0.1)
    elif dur == 130:
        lowPad.stop()
        stutterPadL.fade(0.8, 10)
        stutterPadR.fade(0.8, 10)
    elif dur == 135:
        kickL.play(0.2)
        lowPad.play(0.6)
        grosNoise.play()
        grosNoise.sideChain(1)
        grosNoiseTop.play(0)
        grosNoiseTop.fade(0.8, 4)
    elif dur == 139:
        grosNoiseTop.fade(0, 0.1)
        stutterPadL.fade(0, 0.1)
        stutterPadR.fade(0, 0.1)
    elif dur == 140:
        grosNoiseTop.fade(1, 10)
        stutterPadL.stop()
        stutterPadR.stop()
    elif dur == 150:
        granuleAccu.fade(0, 5)
        grosNoise.randomize(.1, 10)
        f2.play(0)
        f2.fade(0.8, 10)
        kickL.fade(0.9, 30)
        granuleAccu.fade(1.2, 20)
    elif dur == 170:
        f2.randomize(0.2, 1.2)#coupure nette
        kickH.play(0)
        kickH.fade(0.9, 25)
        grosNoise.fade(1.5, 20)
        lowPad.fade(0.9, 25)
    elif dur == 200:
        grosNoiseTop.fade(0, 0.1)
        grosNoise.fade(0, 0.1)
        grosNoisePad.fade(0, 0.1)
        granuleAccu.fade(0, 0.1)
        f2.stop()
        kickH.stop()
        kickL.stop()
        lowPad.fade(0.1, 1)
        douxPadGranule.play(0.2, gen=False)
        douxPadGranule.fade(0.7, 15)
        douxPadGranule.generate(2, 0.5)
        douxPadGranuleAccu1.play(0, gen=False)
        douxPadGranuleAccu2.play(0, gen=False)
        douxPadGranuleAccu1.fade(0.6, 10)
        douxPadGranuleAccu2.fade(0.6, 10)
    elif dur == 205:
        granuleAccu.stop()
        grosNoiseTop.stop()
        grosNoise.stop()
        grosNoisePad.stop()
        lowPad.stop()
    elif dur == 230:
        douxPadGranule.generate(2, 0.5)
        douxPadGranuleAccu1.generate(2, 0.5)
        douxPadGranuleAccu2.generate(2, 0.5)
    elif dur == 250:
        douxPadGranule.fade(1, 5)
        douxPadGranuleAccu1.fade(0.9, 5)
        douxPadGranuleAccu2.fade(0.9, 5)
        stutterPadL.play(0, gen=False)
        stutterPadR.play(0, gen=False)
    elif dur == 260:
        douxPadGranule.fade(0, 0.01)
        arpCrazy.play(0.2, gen=False)
        arpCrazy.fade(0.7, 30)
        stutterPadL.fade(1.5, 2)
        stutterPadL.generate(11, 0.1)
        stutterPadL.drive.time = 0.1
        stutterPadL.drive.value = 0
        stutterPadR.fade(1.5, 2)
        stutterPadR.generate(11, 0.1)
        stutterPadR.drive.time = 0.1
        stutterPadR.drive.value = 0
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
        arpCrazy.generate(4, 0.12)
    elif dur == 320:
        kickCrazy.fade(1, 15)
        kickLFast.fade(1, 20)
        douxPadGranule.generate(2, 0.008)
        douxPadGranuleAccu1.generate(2, 0.007)
        douxPadGranuleAccu2.generate(2, 0.008)
        stutterPadL.drive.time = 25
        stutterPadL.drive.value = 25
        stutterPadR.drive.time = 25
        stutterPadR.drive.value = 25
    elif dur == 340:
        voxyLine.play(0)
        voxyLine.transp=1.8*FLUX
        voxyLine.fade(1, 20)
        voxyLine.fFreq.time = 20
        voxyLine.fFreq.value = 1000
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
        douxPadGranulepitchMod.fade(1, 8)
        douxPadGranuleAccu1pitchMod.fade(1, 8)
        douxPadGranuleAccu2pitchMod.fade(1, 8)
        douxPadGranule.fade(0, 12)
        douxPadGranuleAccu1.fade(0, 12)
        douxPadGranuleAccu2.fade(0, 12)
        arpCrazy.fade(0, 30)
        stutterPadL.fade(0, 30)
        stutterPadR.fade(0, 30)
    elif dur == 365:
        kickCrazy.fade(0, 0.5)
        kickLFast.fade(0, 0.1)
        douxPadGranulepitchMod.fade(0, 1)
        douxPadGranuleAccu1pitchMod.fade(0, 2)
        douxPadGranuleAccu2pitchMod.fade(0, 1)
    elif dur == 370:
        kickLFast.stop()
        kickCrazy.stop()
        arpCrazy.stop()
        douxPadGranulepitchMod.stop()
        douxPadGranuleAccu1pitchMod.stop()
        douxPadGranuleAccu2pitchMod.stop()
    elif dur == 375:
        douxPadGranulepitchMod.play(0, gen=False)
        douxPadGranuleAccu1pitchMod.play(0, gen=False)
        douxPadGranuleAccu2pitchMod.play(0, gen=False)
        douxPadGranulepitchMod.generate(2, 0.004)
        douxPadGranuleAccu1pitchMod.generate(4, 0.09)
        douxPadGranuleAccu2pitchMod.generate(2, 0.06)
        douxPadGranulepitchMod.fade(0.8, 30)
        douxPadGranuleAccu1pitchMod.fade(0.8, 30)
        douxPadGranuleAccu2pitchMod.fade(0.8, 30)
    elif dur == 380:
        stutterPadL.stop()
        stutterPadR.stop()
        douxPadGranule.stop()
        douxPadGranuleAccu1.stop()
        douxPadGranuleAccu2.stop()
    elif dur == 420:
        voxyLine.fade(0, 20)
    elif dur == 450:
        voxyLine.fFreq.time = 0.1
        voxyLine.fFreq.value = 5000
        voxyLine.stop()
        douxPadGranulepitchMod.generate(8, 0.004)
        douxPadGranuleAccu1pitchMod.generate(2, 0.09)
        douxPadGranuleAccu2pitchMod.generate(5, 0.001)
    elif dur == 455:
        voxyLine.play(gen=False)
        voxyLine.generate(5, 0.2)
        voxyLine.fade(0.7, 20)
        voxyLine.fFreq.time = 30
        voxyLine.fFreq.value = 200
        grosNoiseTop.play()
        grosNoiseTop.fFreq.time = 0.1
        grosNoiseTop.fFreq.value = 10000
        grosNoiseTop.fade(1, 30)
        grosNoiseTop.fFreq.time = 30
        grosNoiseTop.fFreq.value = 50
    elif dur == 500:
        transparent.play(0)
        transparentPad.play(0)
        transparentGranule.play(0)
        transparent.fade(0.1, 10)
        transparentPad.fade(0.6, 10)
        transparentGranule.fade(0.7, 10)
        douxPadGranulepitchMod.generate(8, 0.004)
        douxPadGranuleAccu1pitchMod.generate(5, 0.009)
        douxPadGranuleAccu2pitchMod.generate(5, 0.001)
    elif dur == 530:
        voxyLine.fade(0, 20)
        transparent.fade(1, 0.001)
        transparent.fade(0.3, 3)
        transparentPad.fade(0, 20)
        transparentGranule.fade(0, 15)
        douxPadGranulepitchMod.fade(0, 15)
        douxPadGranuleAccu1pitchMod.fade(0, 15)
        douxPadGranuleAccu2pitchMod.fade(0, 15)
    elif dur == 535:
        transparent.fade(0, 10)
    elif dur == 545:
        grosNoiseTop.fFreq.time = 8
        grosNoiseTop.fFreq.value = 20000
        grosNoiseTop.fade(0, 10)
    elif dur == 570:
        grosNoiseTop.stop()
        transparent.stop()
        transparentPad.stop()
        transparentGranule.stop()
        douxPadGranulepitchMod.stop()
        douxPadGranuleAccu1pitchMod.stop()
        douxPadGranuleAccu2pitchMod.stop()


def pp(address, *args):
    global FLUX, BPM
    BPM = args[1]
    FLUX.value = args[0]/1024
    #print(BPM)
    #print(FLUX.value)

r = OscDataReceive(9001, "/BPM", pp)
sender = OscDataSend("iffffff", 18032, '/spat/serv')

def checkBPM():
    BPS.value = (60/BPM) + 1
    BPS.value -= 1
    FLUX.time = BPS
    globalM.time = BPS
    print(BPM)
    print(FLUX.value)

globalM = Metro(time=BPS)
checkBPM = TrigFunc(globalM, checkBPM)
checkTime = TrigFunc(globalM, timeLine)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Gestion des outputs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
padComp = Compress(douxPad.sig()+douxPadGranule.sig()+lowPad.sig()+douxPadGranulepitchMod.sig()+grosNoisePad.sig(), thresh=-24, ratio=6, risetime=.01, falltime=.2, knee=0.5)

padMix = Mix(padComp, mul=0.4).out(0)

percComp = Compress(kickH.sig()+kickL.sig()+granules.sig()+kickCrazy.sig()+kickLFast.sig(), thresh=-24, ratio=6, risetime=.01, falltime=.2, knee=0.5)
percMix = Mix(percComp, mul=0.4).out(1)

sparkMix = Mix(arpCrazy.sig()+voxyLine.sig()+grosNoiseTop.sig()).out(2)

preClip = Clip(grosNoise.sig(), max=1.4, mul=0.8)
noiseMix = Mix(granuleStrecth.sig()+preClip+f2.sig()+granuleAccu.sig(), mul=0.2).out(3)

spatLMix = Mix(douxPadGranuleAccu1.sig()+douxPadGranuleAccu1pitchMod.sig()+stutterPadL.sig(), mul=0.4).out(4)
spatRMix = Mix(douxPadGranuleAccu2.sig()+douxPadGranuleAccu2pitchMod.sig()+stutterPadR.sig(), mul=0.4).out(5)

voxMix = Mix(transparent.sig()+transparentPad.sig()+transparentGranule.sig(), mul=0.3).out(6)

subSplit = EQ(padComp+padMix+sparkMix+noiseMix+spatLMix+spatRMix+voxMix, freq=80, q=1, type=1, mul=0.1)
subComp =Compress(subSplit, thresh=-24, ratio=6, risetime=.01, falltime=.2, knee=0.5)
subMix = Mix(subComp, mul=0.1).mix(2).out(7)
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
msg = [0, 0, pi/2.1, 0.5, .2, 0, 0]
sender.send(msg)
msg = [1, 0, pi/2, 1, 0, 0, 0]
sender.send(msg)
msg = [2, 0, pi/4, 1.5, .3, 0, 0]
sender.send(msg)
msg = [3, 0, pi/2, 1, 0, 0, 0]
sender.send(msg)
msg = [4, pi*1.55, pi/2.15, 0.5, 0.25, 0, 0]
sender.send(msg)
msg = [5, pi/2.25, pi/2.15, 0.5, 0.25, 0, 0]
sender.send(msg)
msg = [6, 0, pi/2, 1, 0, 0, 0]
sender.send(msg)

#s.start()
s.gui(locals())
