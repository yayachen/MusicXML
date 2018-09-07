# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 23:34:57 2018

@author: stanley
"""

import os
import scipy.io
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from plot_confusion_matrix import plot_confusion_matrix
import matplotlib.pyplot as plt
from collections import Counter

pitchscale = {'C':0,'C#':1,'D':2,'D#':3,
              'E':4,'F':5,'F#':6,'G':7,
              'G#':8,'A':9,'A#':10,'B':11}
key = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'
       ,'a','a#','b','c','c#','d','d#','e','f','f#','g','g#'] 
chord_template = ['maj','7','min','dim']#,'xxx','X'] 
pitchclass = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']  
chord_number = [ p+':'+t  for t in chord_template for p in pitchclass]
#root = r'C:\Users\stanley\Desktop\SCREAM Lab'
#path = r'YA\code\key_analysis\key_result\pei'

def readmatfile(filepath):
    #mat = scipy.io.loadmat('\\'.join((root,path,file)))['data'] #load matfile
    mat = scipy.io.loadmat(filepath)['data']
    d1,d2 = mat.shape   # 取每維度大小
    for i in range(d1): # 資料精簡
        for j in range(d2):
            try:
                mat[i][j] = mat[i][j].item()
            except ValueError:
                continue
    mat = pd.DataFrame(mat) #轉pandas才能開
    return mat

def getKeyeachBar(data):
    #key_data = np.zeros(len(data),dtype = np.dtype((str, 2)))
    key_data = ['']*len(data)
    for i in range(1,len(data)):
        bar_index = data[0][i]
        key_data[bar_index] = data[2][i]
    #key_data = key_data[key_data != '']
    key_data = [ x for x in key_data if x != '']
    return key_data

def getChord(data,frame_size = 0.125):
    beat = 6 if max(data[1][1:]) >= 4 else 4  # 4/4 or 6/8  #第一個是 字串
    
    Chord_data = []#['']*len(data)
    for i in range(1,len(data)):
        try:
            duration = (data[0][i+1] - data[0][i])*beat/frame_size + ((data[1][i+1] - data[1][i])/frame_size) # data[0]小節 data[1]拍
        except KeyError:   #最後一小節
            duration = ((beat - data[1][i])/frame_size)
        Chord_data += [data[3][i]]*int(duration)
        #Chord_data[bar_index] = data[3][i]
    #Chord_data = [ x for x in key_data if x != '']
    return Chord_data
    
if __name__== "__main__":    
    r_dir = r'C:\Users\stanley\Desktop\SCREAM Lab\YA\code\key_analysis\key_result\pei'   #root+'\\'+path
    chord_result = []
    chord_GT = []
    for root, sub, files in os.walk(r_dir):
        files = sorted(files)
    
        for f in files:       
            base=os.path.basename(f)
            print(base)
            filepath = root+"\\"+base
            data = readmatfile(filepath)
            if root.split('\\')[-1] != 'chordGT':
                chord_result.append(getChord(data))
            else:
                chord_GT.append(getChord(data))
    cm = []
    for i in range(len(chord_GT)):
        cm.append(confusion_matrix(chord_GT[i], chord_result[i],labels = chord_number)) #, ignore_index=True
    ALLcm = sum(cm)    

    """
    # plot_confusion_matrix all
    plt.figure(figsize=(10, 10))
    plot_confusion_matrix(ALLcm, classes=chord_number,
                      title='Chords Confusion matrix')
    plt.savefig('Chords Confusion matrix.png', dpi=600,bbox_inches="tight")

    plt.figure(figsize=(10, 10))
    plot_confusion_matrix(ALLcm, classes=chord_number, normalize=True,
                      title='Chords Normalized confusion matrix')
    plt.savefig('Chords Normalized confusion matrix', dpi=600,bbox_inches="tight")
    """    
    
    chord_quality_result = [ ch.split(":")[-1] for song in chord_result for ch in song]
    chord_quality_GT = [ ch.split(":")[-1] for song in chord_GT  for ch in song]
    chord_root_result = [ ch.split(":")[0] for song in chord_result for ch in song]
    chord_root_GT = [ ch.split(":")[0] for song in chord_GT  for ch in song]
    
    quality_cm = confusion_matrix(chord_quality_result, chord_quality_GT,labels = chord_template)
    root_cm = confusion_matrix(chord_root_result, chord_root_GT,labels = pitchclass)
    
    #relative =[ (pitchclass.index(chord_root_result[i]) - pitchclass.index(chord_root_GT[i]) ) %12 for i in range(len(chord_root_GT))]
    relative = []
    for i in range(len(chord_root_GT)):
        try:
            relative.append((pitchclass.index(chord_root_result[i]) - pitchclass.index(chord_root_GT[i]) ) %12)
        except ValueError:
            continue
    relative_cnf = [relative.count(x) for x in range(len(pitchclass))]
    relative_cnf = np.array(relative_cnf )/sum(relative_cnf )    
    
    """
    # plot_confusion_matrix quality root
    plt.figure()
    plot_confusion_matrix(quality_cm, classes=chord_template,
                      title='Chords quality Confusion matrix')
    plt.savefig('Chords quality Confusion matrix.png', dpi=500,bbox_inches="tight")

    plt.figure()
    plot_confusion_matrix(quality_cm, classes=chord_template, normalize=True,
                      title='Chords quality Normalized confusion matrix')
    plt.savefig('Chords quality Normalized confusion matrix', dpi=500,bbox_inches="tight")
    
    # root
    plt.figure(figsize=(8, 8))
    plot_confusion_matrix(root_cm, classes=pitchclass,
                      title='Chords root Confusion matrix')
    plt.savefig('Chords root Confusion matrix.png', dpi=500,bbox_inches="tight")

    plt.figure(figsize=(8, 8))
    plot_confusion_matrix(root_cm, classes=pitchclass, normalize=True,
                      title='Chords root Normalized confusion matrix')
    plt.savefig('Chords root Normalized confusion matrix', dpi=500,bbox_inches="tight")
    """
    
    """
    cm = []
    relative = []
    for i in range(len(chord_GT)):
        cm.append(confusion_matrix(chord_GT[i], chord_result[i],labels = key)) #, ignore_index=True
        relative+=([ (key.index(chord_result[i][j]) - key.index(chord_GT[i][j]) ) %24
                             for j in range(len(chord_GT[i]))])
    ALLcm = sum(cm)
    #relative_cnf = [relative.count(x) for x in range(len(key))]
    #relative_cnf = np.array(relative_cnf )/sum(relative_cnf )
    """

    
    # plt relative
    plt.figure()
    plt.bar(range(len(pitchclass)),relative_cnf)
    plt.xticks(range(len(pitchclass)), pitchclass)
    plt.xlabel("Pitchclass")
    plt.ylabel("Probability")
    plt.title('Relative Chords root Predict')
    plt.savefig('Relative Chords root Predict', dpi=200,bbox_inches="tight")
    