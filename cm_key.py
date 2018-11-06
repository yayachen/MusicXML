# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 23:37:17 2018

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

def plot_bar(data,xticks,title):
    
    data = [data.count(x) for x in range(len(key))]
    data = np.array(data )/sum(data )
    
    # plot
    plt.figure()
    plt.bar(range(len(xticks)),data)
    plt.xticks(range(len(xticks)), xticks)
    plt.xlabel("Keys")
    plt.ylabel("Probability")
    plt.title(title)
    plt.savefig(title+'.png', dpi=200,bbox_inches="tight")
    
if __name__== "__main__":    
    r_dir = r'C:\Users\stanley\Desktop\SCREAM Lab\YA\code\key_analysis\key_result\pei'   #root+'\\'+path
    key_result = []
    key_GT = []
    for root, sub, files in os.walk(r_dir):
        files = sorted(files)
    
        for f in files:       
            base=os.path.basename(f)
            print(base)
            if base != 'c_40_1.mat':continue
            filepath = root+"\\"+base
            data = readmatfile(filepath)
            if root.split('\\')[-1] != 'chordGT':
                key_result.append(getKeyeachBar(data))
            else:
                key_GT.append(getKeyeachBar(data))
    
    cm = []
    relative = []
    Moveable_Do_major = []
    Moveable_Do_minor = []
    for i in range(len(key_GT)):
        cm.append(confusion_matrix(key_GT[i], key_result[i],labels = key)) #, ignore_index=True
        relative+=([ (key.index(key_result[i][j]) - key.index(key_GT[i][j]) ) %24
                             for j in range(len(key_GT[i]))])
        for j in range(len(key_GT[i])) :
            if key_GT[i][j].isupper():
                if key_result[i][j].isupper():
                    Moveable_Do_major += [(key.index(key_result[i][j]) - key.index(key_GT[i][j]) ) %12]
                else:
                    Moveable_Do_major += [(key.index(key_result[i][j]) - key.index(key_GT[i][j]) - 12 ) %12 + 12]
                
            else:
                if key_result[i][j].islower():
                    Moveable_Do_minor += [(key.index(key_result[i][j]) - key.index(key_GT[i][j]) ) %12]
                else:
                    Moveable_Do_minor += [(key.index(key_result[i][j]) - key.index(key_GT[i][j]) - 12 ) %12 + 12]
                        
                
    ALLcm = sum(cm)
    
    
    #plot_bar(relative,key,'Relative Key Predict')
    #plot_bar(Moveable_Do_major,key,'Moveable_Do_major Predict')
    #plot_bar(Moveable_Do_minor,key[12:]+key[:12],'Moveable_Do_minor Predict')
""" 
    # plot_confusion_matrix
    plt.figure(figsize=(8, 8))
    plot_confusion_matrix(ALLcm, classes=key,
                      title='Keys Confusion matrix')
    plt.savefig('Keys Confusion matrix.png', dpi=500,bbox_inches="tight")

    plt.figure(figsize=(8, 8))
    plot_confusion_matrix(ALLcm, classes=key, normalize=True,
                      title='Keys Normalized confusion matrix')
    plt.savefig('Keys Normalized confusion matrix', dpi=500,bbox_inches="tight")
       

    plt.figure()
    plt.bar(range(len(key)),relative_cnf)
    plt.xticks(range(len(key)), key)
    plt.xlabel("Keys")
    plt.ylabel("Probability")
    plt.title('Relative Key Predict')
    plt.savefig('Relative Key Predict.png', dpi=200,bbox_inches="tight")
"""
