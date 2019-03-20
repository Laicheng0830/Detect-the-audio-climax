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
            times = determine_audio(audio,fs)
            if len(times) > 0:
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
    length = fs*1
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
    data_n = np.zeros(corr_N.shape)
    flag = np.zeros(N)

    for i in range(N-1):
        for j in range(i+1,N):
            if corr_N[i][j] > corr_N_max:
                corr_N_max = corr_N[i][j]
                corr_N_max_id = [i+1,j+1]
            if corr_N[i][j] > 0.8:
                data_n[i][j] = corr_N[i][j]
                flag[j] = 5

    # If you're greater than 0 on both sides, you take the middle out
    for i in range(1,len(flag)-1):
        if flag[i-1] > 0 and flag[i+1] > 0:
            flag[i] = flag[i-1]

    # Let's get rid of the 0's on both sides
    for i in range(1,len(flag)-1):
        if flag[i-1] == 0 and flag[i+1] == 0:
            flag[i] = 0


    count_linear = 0
    times = []
    for i in range(len(flag)-1):
        if flag[i] > 0:
            count_linear += 1
            if flag[i+1] == 0:
                end = i
                start = end - count_linear
                # print("linear 1:",count_linear,"start end :",start,end)
                if count_linear >= 10:
                    times.append([start,end])
                count_linear = 0

    print("select times:",times)
    # print("corr max and id",corr_N_max,corr_N_max_id)
    # print(corr_N.shape)
    # plt.plot(flag,'w')
    # plt.imshow(data_n)
    # plt.colorbar()
    # plt.show()
    return times


if __name__ == '__main__':
    read_dir()
