#!/usr/bin/env python3

"""
This script is to extract and store excited state information.
"""

import numpy as np

from glob import glob
import sys

def extract_store(data_source, store_file, threshold=None):
    tdDataFile = data_source

    tdWavl = []
    tdStrength = []
    tdID = []

    with open(tdDataFile, 'r') as f:
        lines = f.read().splitlines()
        current_wavl = []
        current_strength = []
    
        for line in lines:
            splitL = line.split()
            if len(splitL) == 0:
                if current_wavl and current_strength:
                    tdWavl.append(current_wavl)
                    tdStrength.append(current_strength)
                current_wavl = []
                current_strength = []
            elif len(splitL) == 1:
                if current_wavl and current_strength:
                    tdWavl.append(current_wavl)
                    tdStrength.append(current_strength)
                current_wavl = []
                current_strength = []
                tdID.append(splitL[0])
            elif len(splitL) == 2:
                current_wavl.append(float(splitL[0]))
                current_strength.append(float(splitL[1]))

        if current_wavl and current_strength:
            tdWavl.append(current_wavl)
            tdStrength.append(current_strength)

    tdID = np.array(tdID)
    tdWavl = np.array(tdWavl)
    tdStrength = np.array(tdStrength)
    
    if threshold is not None:
        tdID, tdWavl, tdStrength = apply_filter(tdID, tdWavl, tdStrength, threshold)

    np.savez(f'{store_file}.npz', 
             id=tdID, 
             wavl=tdWavl, 
             strength=tdStrength)

def apply_filter(id, walv, strength, threshold):
    tdWavl = []
    tdStrength = []
    tdID = []

    for i, w, s in zip(id, walv, strength,):
        if (w > threshold).any():
            tdID.append(i)
            tdWavl.append(w)
            tdStrength.append(s)

    tdID = np.array(tdID).reshape(-1,1)
    tdWavl = np.array(tdWavl)
    tdStrength = np.array(tdStrength)

    return tdID, tdWavl, tdStrength

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 3:
        data_source = args[1]
        store_file = args[2]
        extract_store(data_source, store_file)
    if len(args) == 4:
        data_source = args[1]
        store_file = args[2]
        threshold = args[2]
        extract_store(data_source, store_file, threshold)
    else:
        print(f'usage: {args[0]} data_source store_file threshold (optional)')
        print(f'threshold: wavelength filter, e.g., 200, 250.')
        exit