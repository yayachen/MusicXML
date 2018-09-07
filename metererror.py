# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 16:34:03 2018

@author: stanley
"""
from music21 import *
import xlrd
import pyfpgrowth
from collections import Counter
import matplotlib.pyplot as plt


template = {'maj':(0,4,7),
            'min':(0,3,7),
            'dim':(0,3,6),
            '7'  :(0,4,7,10),
            'dim7':(0,3,6,9),
            'min7':(0,3,7,9)
            }
pitchscale = {'C':0,'C#':1,'D':2,'D#':3,
              'E':4,'F':5,'F#':6,'G':7,
              'G#':8,'A':9,'A#':10,'B':11}
              
Voicing = {}
for t in list(template.keys()):
        Voicing[t] =[]#{}
Voicing_patterns = {}
Voicing_rules = {}
Voicing_count = {}
error = 0

def VoicingAnalyze(songpath,songname):  
    global error
    # read groundtruth chord ('trans_'+songname
    # gtChords [Measure,Beat,[pitchs]]
    # gtChords [Measure,Beat,rootpitch,quality]
    xlsxdata = xlrd.open_workbook(songpath+'trans_'+songname+'.xlsx')
    table = xlsxdata.sheets()[0]
    nrows = table.nrows
    gtChords = [[]+[]*int(table.row_values(nrows-1)[0])]  
    gtChords = [[] for i in range(int(table.row_values(nrows-1)[0])+1)]
    for i in range(1,nrows):
        try:
            rootpitch,quality = table.row_values(i)[3].split(':')
        #gtChords.setdefault(table.row_values(i)[0],default=[])
        #gtChords.append(table.row_values(i)[1]+[rootpitch]+[quality])
            gtChords[int(table.row_values(i)[0])].append([table.row_values(i)[1]]+[rootpitch]+[str(quality)])
        #print(gtChords[int(table.row_values(i)[0])])
        except ValueError :
            gtChords[int(table.row_values(i)[0])].append([table.row_values(i)[1]]+['special']+['special'])
    
    # read musicXml chord (songname
    # Chordlist [Measure,Beat,[pitchs]]

    xmldata = converter.parse(songpath+songname+'.xml')
    xmlChords = xmldata.chordify()
    Chordlist = []
    #xmlChords.measures(1, 65).recurse().getElementsByClass('Chord'):
    shift = 0  ##先行小節的問題 對不上學姊標記的trans
    for thisChord in xmlChords.recurse().getElementsByClass('Chord'):
        if thisChord.measureNumber == 0:
            shift = 1
        try:
            Chordlist.append([thisChord.measureNumber+shift, thisChord.beat-1.0,thisChord.pitchClasses])#thisChord.pitchedCommonName)
        except meter.MeterException:
            error +=1
            continue
        #print(Chordlist[-1])
        
    ##
    for m,b,p in  Chordlist:
        #print(m,b,p)
        temp = -1  ##代表gtChords 該小節中的哪一個
        for i in range(len(gtChords[m])):
            if b >= gtChords[m][i][0] :
                temp +=1
        #print(temp)
        if gtChords[m][temp][1] == 'special':
            break
        rootpitch = gtChords[m][temp][1]
        quality = gtChords[m][temp][2]
        #tempvoicing = sorted(list(map(lambda x:(x-pitchscale[rootpitch])%12,p)))
        tempvoicing = list(map(lambda x:(x-pitchscale[rootpitch])%12,p))
        #print(type(quality.strip()),tempvoicing)
        Voicing[quality].append(tempvoicing)
    return Voicing
              
if __name__== "__main__":
    peipath = "C:/Users/stanley/Desktop/SCREAM Lab/np&pd/DETECTION OF KEY CHANGE IN CLASSICAL PIANO MUSIC/midi/pei/"
    #songlist = ['m_16_1','b_4_2','b_20_1','b_20_2','c_40_1','c_47_1',
    #       'h_23_1','h_37_1','h_37_2','m_7_1','m_7_2','m_16_1','m_16_2']
    #songlist = ['m_16_1','b_20_1','b_20_2','c_47_1',
    #       'h_23_1','h_37_1','h_37_2','m_7_1','m_7_2','m_16_1','m_16_2']
    songlist = ['b_4_2','c_40_1']
    for s in songlist:
        print(s)
        test = VoicingAnalyze(peipath,s)  
        print(error)
    #AssociationRule(Voicing,0,0.2)
    #Count_voicing(Voicing)
    [ plot_bar(key) for key in Voicing_count.keys() ]