# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 18:57:44 2018

@author: stanley
"""

from music21 import *
songname = "C:/Users/stanley/Desktop/SCREAM Lab/np&pd/DETECTION OF KEY CHANGE IN CLASSICAL PIANO MUSIC/midi/pei/b_4_1.xml"
song = converter.parse(songname)
TS = song.recurse().getElementsByClass('TimeSignature')[0]
print(song.recurse().getElementsByClass('TimeSignature')[0])
if TS.ratioString == '6/8':
    print('6/8')
    #fast2slow = 6/song.measure(0).beatCount
    #song.measure(0).timeSignature = meter.TimeSignature('slow 6/8')
    #song.measure(0).beatCount = 6 
    #song.quarterLength = 0.5
print(song.recurse().getElementsByClass('TimeSignature')[0])
xmlChords = song.chordify()
Chordlist = []
#xmlChords.measures(1, 65).recurse().getElementsByClass('Chord'):
TS = song.recurse().getElementsByClass('TimeSignature')[0]
fast2slow = 6/TS.beatCount if TS.ratioString == '6/8' else 1
shift = 0  ##先行小節的問題 對不上學姊標記的trans
for thisChord in xmlChords.recurse().getElementsByClass('Chord'):
    if thisChord.measureNumber == 0:
        shift = 1
    try:
        Chordlist.append([thisChord.measureNumber+shift, round(fast2slow*(thisChord.beat-1.0),1),thisChord.pitchClasses])#thisChord.pitchedCommonName)
    except meter.MeterException:
        error +=1
        continue
    print(Chordlist[-1])