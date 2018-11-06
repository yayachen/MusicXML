# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 12:55:23 2018

@author: stanley
"""

import os
import re
import pathlib
from music21 import *

allF = musicxml.lilypondTestSuite.allFiles()
untested = [f.name for f in sorted(allF)]
scores = {}
musicxmlOut = {}

def s(i):
    if isinstance(i, int):
        longFp = allF[i]
    else:
        for longFp in allF:
            shortFp = longFp.name
            if i in shortFp:
                break
        else:
            raise Exception("Cannot find: " + str(i))
    shortFp = longFp.name
    if shortFp in untested:
        untested.remove(shortFp)

    sc = converter.parse(longFp, forceSource=True)
    scores[i] = sc

    fp = pathlib.Path(sc.filePath).name
    print(fp + '\n')

    desc = sc.metadata.description
    desc = re.sub(r'\s+', ' ', desc)
    print(desc)

    fpOut = sc.write('musicxml')
    with open(fpOut, 'r') as musicxmlOutFile:
        allOut = musicxmlOutFile.read()

    musicxmlOut[i] = allOut
    return sc.show()