# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 15:44:23 2018

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

#Voicing = {}
#for t in list(template.keys()):
        #Voicing[t] =[]#{}
#Voicing_patterns = {}
#Voicing_rules = {}
#Voicing_count = {}


def init():
    global Voicing
    global Voicing_patterns
    global Voicing_rules
    global Voicing_count
    Voicing = {}
    for t in list(template.keys()):
        Voicing[t] =[]#{}
    Voicing_patterns = {}
    Voicing_rules = {}
    Voicing_count = {}
    
def VoicingAnalyze(songpath,songname):  
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
            gtChords[int(table.row_values(i)[0])].append([table.row_values(i)[1]]+[rootpitch]+[str(quality)])
        except ValueError :
            gtChords[int(table.row_values(i)[0])].append([table.row_values(i)[1]]+['special']+['special'])
    
    # read musicXml chord (songname
    # Chordlist [Measure,Beat,[pitchs]]

    xmldata = converter.parse(songpath+songname+'.xml')
    xmlChords = xmldata.chordify()
    Chordlist = []
    #xmlChords.measures(1, 65).recurse().getElementsByClass('Chord'):
    TS = xmldata.recurse().getElementsByClass('TimeSignature')[0]  ##拍號
    fast2slow = 6/TS.beatCount if TS.ratioString == '6/8' else 1  ## 6/8拍問題，學姊標記是用slow，midi讀到是fast
    shift = 0  ##先行小節的問題 對不上學姊標記的trans
    for thisChord in xmlChords.recurse().getElementsByClass('Chord'):
        if thisChord.measureNumber == 0:
            shift = 1
        try:
            Chordlist.append([thisChord.measureNumber+shift, round(fast2slow*(thisChord.beat-1.0),1),thisChord.pitchClasses])#thisChord.pitchedCommonName)
        except meter.MeterException:
            continue
        #print(Chordlist[-1])
    print(len(Chordlist))    
    ##
    for m,b,p in  Chordlist:
        #print(m,b,p)
        temp = -1  ##代表gtChords 該小節中的哪一個
        for i in range(len(gtChords[m])):
            if b >= gtChords[m][i][0] :
                temp +=1
        #print(temp)
        if gtChords[m][temp][1] == 'special':
            continue
        rootpitch = gtChords[m][temp][1]
        quality = gtChords[m][temp][2]
        #tempvoicing = sorted(list(map(lambda x:(x-pitchscale[rootpitch])%12,p)))
        tempvoicing = list(map(lambda x:(x-pitchscale[rootpitch])%12,p))
        #print(type(quality.strip()),tempvoicing)
        Voicing[quality].append(tempvoicing)
    return Voicing

def AssociationRule(Voicing,support,confidence):
    #Voicing_patterns = {}
    #Voicing_rules = {}
    for v in Voicing.items():
        patterns = pyfpgrowth.find_frequent_patterns(v[1], len(v[1])*support)
        Voicing_patterns[v[0]] = patterns
        rules = pyfpgrowth.generate_association_rules(patterns, confidence)
        Voicing_rules[v[0]]= rules
    return Voicing_patterns,Voicing_rules

def Count_voicing(Voicing):
    #Voicing_count = {}
    for v in Voicing.items():
        Voicing_count[v[0]] = Counter(sum(v[1],[]))
        Voicing_count[v[0]] = { key: val/len(v[1]) for key,val in Voicing_count[v[0]].items()}
    return Voicing_count 

def plot_bar(quality):
    data = Voicing_count[quality]
    #key,values = data
    plt.figure(figsize=(9, 7))
    plt.xlabel("Interval")
    plt.ylabel("Proportion")
    plt.title(quality+" "+str(len(Voicing[quality])))
    data = sorted(data.items(), key=lambda d: d[1],reverse=True)
    names,values = zip(*data)
    plt.bar(range(len(data)),values,tick_label=names)
    plt.savefig("Voicing_"+quality+".png",dpi = 300)
    
if __name__== "__main__":
    peipath = "C:/Users/stanley/Desktop/SCREAM Lab/np&pd/DETECTION OF KEY CHANGE IN CLASSICAL PIANO MUSIC/midi/pei/"
    #songlist = ['m_16_1','b_4_2','b_20_1','b_20_2','c_40_1','c_47_1',
    #       'h_23_1','h_37_1','h_37_2','m_7_1','m_7_2','m_16_1','m_16_2']
    songlist = ['m_16_1','b_4_1','b_4_2','b_20_1','b_20_2','c_40_1','c_47_1',
           'h_23_1','h_37_1','h_37_2','m_7_1','m_7_2','m_16_1','m_16_2']
    #songlist = ['c_40_1']
    init()
    for s in songlist:
        print(s)
        VoicingAnalyze(peipath,s)  
    AssociationRule(Voicing,0,0.2)
    Count_voicing(Voicing)
    [ plot_bar(key) for key in Voicing_count.keys() ]
    
    


        