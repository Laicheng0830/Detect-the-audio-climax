"""
!/usr/bin/env python
-*- coding:utf-8 -*-
Author: eric.lai
Created on 2019/3/15 11:09
"""

import numpy as np
import os,soundfile,librosa
import matplotlib.pylab as plt

# parameter config
DIR_PATH = 'E:/Low_frequency_wav/'

def read_dir(dir = DIR_PATH):
    count = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = dir + str(file)
            print(file_path)
            audio, fs = read_audio(file_path)
            audio = silence_detection(audio)
            corr_max,max_id1,max_id2 = determine_audio(audio,fs)
            if corr_max>0.6:
                count += 1
    print(count/671,"count")

def read_audio(path, target_fs=None):
    """read audio"""
    (audio, fs) = soundfile.read(path)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    if target_fs is not None and fs != target_fs:
        audio = librosa.resample(audio, orig_sr=fs, target_sr=target_fs)
        fs = target_fs
    return audio, fs

def silence_detection(data):
    start = 0
    for i in range(441000):
        if abs(data[i])<1e-3:
            continue
        else:
            start = i
            break
    return data[start:]

def determine_audio(data,fs):
    length = fs*10
    N = int(len(data)/length)
    data_N = np.zeros((N,length))
    start = 0
    end = length
    for i in range(N):
        data_N[i] = data[start:end]
        start = end
        end += length
    # print(data_N.shape)
    corr_N = np.corrcoef(data_N)
    corr_N_max = 0
    corr_N_max_id = [0,0]
    data_n = np.ones(corr_N.shape)
    for i in range(N-1):
        for j in range(i+1,N):
            if corr_N[i][j] > corr_N_max:
                corr_N_max = corr_N[i][j]
                corr_N_max_id = [i+1,j+1]
            data_n[i][j] = corr_N[i][j]

    time1 = divmod(corr_N_max_id[0]*10,60)
    time2 = divmod(corr_N_max_id[1]*10,60)
    print("start times:",time1,time2)
    print("corr max and id",corr_N_max,corr_N_max_id)
    print(corr_N.shape)
    plt.imshow(data_n)
    plt.colorbar()
    plt.show()
    return corr_N_max,corr_N_max_id[0]-1,corr_N_max_id[1]-1


if __name__ == '__main__':
    read_dir()
