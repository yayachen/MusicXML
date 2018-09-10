# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 16:18:30 2018

@author: stanley
"""
import csv
csv_attribute = ['小節','拍數(onset)','調性','和弦級數','和弦編號','備註']
major_mode = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
minor_mode = ['a','a#','b','c','c#','d','d#','e','f','f#','g','g#']

              
def shift_groundtruth(GTfile,shift):
    # read csv 
    with open(GTfile, newline='') as csvfile:
        rows = csv.reader(csvfile)
        rowdata = [ row for row in rows]
    # shift data
    for i in range(1,len(rowdata)):
        # shift key
        if rowdata[i][2].isupper():
            rowdata[i][2] = major_mode[(major_mode.index(rowdata[i][2])+shift)%12]
        else :
            rowdata[i][2] = minor_mode[(minor_mode.index(rowdata[i][2])+shift)%12]
        # shift chord
        root = rowdata[i][3].split(':')[0]
        rowdata[i][3] = rowdata[i][3].replace(root,major_mode[(major_mode.index(root)+shift)%12])
        # shift number
        quality = (int(rowdata[i][4])-1)//12
        rowdata[i][4] = str(12*quality+((int(rowdata[i][4])+shift-1)%12)+1)  # index 不是從0開始是從1 , 所以要mod12要先-1再+1
    return rowdata

if __name__== "__main__":    
    rootpath = r'../../YA/code/annotation'
    songname = '/trans_m_16_1.csv'
    shift = 4
    rowdata = shift_groundtruth(rootpath+songname,shift)
    
    # write csv
    outputname = songname.split('.')[0]+'_'+str(shift)+'.csv'
    with open( rootpath+outputname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rowdata)
    