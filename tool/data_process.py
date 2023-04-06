# -*- coding: utf-8 -*-
# @Time : 2023/1/10 20:36
# @Author : hzkuang
# @Project : HLSDSE
# @File : data_process.py

import os
import json
import numpy as np
from pareto import *


# Constant
WLUT: float = 0.3
WFF: float = 0.25
WDSP: float = 0.3
WBRAM: float = 0.05
WURAM: float = 0.05
WSRL: float = 0.05


def getListPPA(path):
    listPPA = []
    for file in os.listdir(path):
        if file.split('_')[0] == 'ppa':
            file_path = os.path.join(path, file)
            listPPA.append(file_path)
    listPPA.sort(key=lambda x: (int((x.split('_')[-1]).split('.')[0])))
    return listPPA


if __name__ == "__main__":
    wght = [WLUT, WFF, WDSP, WBRAM, WURAM, WSRL]

    nameList = ['aes', 'bfs_bulk', 'fft_strided', 'gemm_ncubed', 'md_knn', 'nw', 'sort_radix', 'spmv_ellpack',
                'stencil3d', 'viterbi']
    folderList = ['aes/aes', 'bfs/bulk', 'fft/strided', 'gemm/ncubed', 'md/knn', 'nw/nw', 'sort/radix', 'spmv/ellpack',
                  'stencil/stencil3d', 'viterbi/viterbi']
    powerList = [0.361, 0.249, 0.301, 0.308, 1.516, 0.258, 0.253, 0.314, 0.278, 0.426]
    cpList = [7.742, 3.804, 9.064, 7.788, 9.716, 4.763, 4.189, 7.631, 6.187, 9.122]
    latList = [713, 1000, 1000, 131369, 2467, 1000, 166289, 2529, 1000, 294737]
    areaList = [5274, 288.7, 1343.8, 4372.7, 22513.45, 445.8, 1313.15, 1727.75, 310.9, 13590.55]

    perfList = [cp * lat for cp, lat in zip(cpList, latList)]

    index = 9
    name = nameList[index]
    bench = folderList[index]
    power = powerList[index]
    perf = perfList[index]
    area = areaList[index]

    dataset_path = os.path.abspath("../dataset/MachSuite")
    path_bo = os.path.join(dataset_path, 'dataset_motpe', bench, 'script')
    path_ga = os.path.join(dataset_path, 'dataset_nsga', bench, 'script')
    path_sa = os.path.join(dataset_path, 'dataset_sa', bench, 'script')
    path_ds = os.path.join(dataset_path, 'dataset_discrete', bench, 'script')
    listPPA_bo = getListPPA(path_bo)
    listPPA_ga = getListPPA(path_ga)
    listPPA_sa = getListPPA(path_sa)
    listPPA_ds = getListPPA(path_ds)
    listPPA = listPPA_bo + listPPA_ga + listPPA_sa + listPPA_ds
    inputPoints_bo = []
    inputPoints_ga = []
    inputPoints_sa = []
    inputPoints_ds = []
    inputPoints = []

    # get pareto points for reference set
    for dir in listPPA:
        f = open(dir)
        data = json.load(f)
        if data['IMPL']['PWR'] == 1e8:
            print(dir)
        else:
            usg = [data['IMPL']['LUT'], data['IMPL']['FF'], data['IMPL']['DSP'], data['IMPL']['BRAM'],
                   data['IMPL']['URAM'], data['IMPL']['SRL']]
            power = data['IMPL']['PWR']
            perf = data['IMPL']['CP'] * data['LATENCY']['Latency']
            area = sum(np.multiply(wght, usg))
            inputPoints.append([power, perf, area])
    paretoPoints, dominatedPoints = simple_cull(inputPoints, dominates)

    # get pareto points for MOTPE-F
    for dir in listPPA_bo:
        f = open(dir)
        data = json.load(f)
        if data['IMPL']['PWR'] == 1e8:
            print(dir)
        else:
            usg = [data['IMPL']['LUT'], data['IMPL']['FF'], data['IMPL']['DSP'], data['IMPL']['BRAM'],
                   data['IMPL']['URAM'], data['IMPL']['SRL']]
            power = data['IMPL']['PWR']
            perf = data['IMPL']['CP'] * data['LATENCY']['Latency']
            area = sum(np.multiply(wght, usg))
            inputPoints_bo.append([power, perf, area])
    paretoPoints_bo, dominatedPoints_bo = simple_cull(inputPoints_bo, dominates)

    # get pareto points for MOTPE-D
    for dir in listPPA_ds:
        f = open(dir)
        data = json.load(f)
        if data['IMPL']['PWR'] == 1e8:
            print(dir)
        else:
            usg = [data['IMPL']['LUT'], data['IMPL']['FF'], data['IMPL']['DSP'], data['IMPL']['BRAM'],
                   data['IMPL']['URAM'], data['IMPL']['SRL']]
            power = data['IMPL']['PWR']
            perf = data['IMPL']['CP'] * data['LATENCY']['Latency']
            area = sum(np.multiply(wght, usg))
            inputPoints_ds.append([power, perf, area])
    paretoPoints_ds, dominatedPoints_ds = simple_cull(inputPoints_ds, dominates)

    # get pareto points for NSGA
    for dir in listPPA_ga:
        f = open(dir)
        data = json.load(f)
        if data['IMPL']['PWR'] == 1e8:
            print(dir)
        else:
            usg = [data['IMPL']['LUT'], data['IMPL']['FF'], data['IMPL']['DSP'], data['IMPL']['BRAM'],
                   data['IMPL']['URAM'], data['IMPL']['SRL']]
            power = data['IMPL']['PWR']
            perf = data['IMPL']['CP'] * data['LATENCY']['Latency']
            area = sum(np.multiply(wght, usg))
            inputPoints_ga.append([power, perf, area])
    paretoPoints_ga, dominatedPoints_ga = simple_cull(inputPoints_ga, dominates)

    # get pareto points for SA
    for dir in listPPA_sa:
        f = open(dir)
        data = json.load(f)
        if data['IMPL']['PWR'] == 1e8:
            print(dir)
        else:
            usg = [data['IMPL']['LUT'], data['IMPL']['FF'], data['IMPL']['DSP'], data['IMPL']['BRAM'],
                   data['IMPL']['URAM'], data['IMPL']['SRL']]
            power = data['IMPL']['PWR']
            perf = data['IMPL']['CP'] * data['LATENCY']['Latency']
            area = sum(np.multiply(wght, usg))
            inputPoints_sa.append([power, perf, area])
    paretoPoints_sa, dominatedPoints_sa = simple_cull(inputPoints_sa, dominates)

    print("*" * 8 + " Reference Set " + "*" * 8)
    print("non-dominated answers")
    print('number: ' + str(len(paretoPoints)))
    for p in paretoPoints:
        print(p)

    print("*" * 8 + " MOTPE-F Pareto Front " + "*" * 8)
    print("non-dominated answers")
    print('number: ' + str(len(paretoPoints_bo)))
    listLPDA_bo = []
    lpda_bo = 0
    for p in paretoPoints_bo:
        print(p)
        value = p[0] * p[1] * p[2]
        lpda_bo += value
        listLPDA_bo.append(value)
    lpda_bo = lpda_bo/len(paretoPoints_bo)
    min_lpda_bo = min(listLPDA_bo)

    print("*" * 8 + " MOTPE-D Pareto Front " + "*" * 8)
    print("non-dominated answers")
    print('number: ' + str(len(paretoPoints_ds)))
    listLPDA_ds = []
    lpda_ds = 0
    for p in paretoPoints_ds:
        print(p)
        value = p[0] * p[1] * p[2]
        lpda_ds += value
        listLPDA_ds.append(value)
    lpda_ds = lpda_ds / len(paretoPoints_ds)
    min_lpda_ds = min(listLPDA_ds)

    print("*" * 8 + " NSGA Pareto Front " + "*" * 8)
    print("non-dominated answers")
    print('number: ' + str(len(paretoPoints_ga)))
    listLPDA_ga = []
    lpda_ga = 0
    for p in paretoPoints_ga:
        print(p)
        value = p[0] * p[1] * p[2]
        lpda_ga += value
        listLPDA_ga.append(value)
    lpda_ga = lpda_ga/len(paretoPoints_ga)
    min_lpda_ga = min(listLPDA_ga)

    print("*" * 8 + " SA Pareto Front " + "*" * 8)
    print("non-dominated answers")
    print('number: ' + str(len(paretoPoints_sa)))
    listLPDA_sa = []
    lpda_sa = 0
    for p in paretoPoints_sa:
        print(p)
        value = p[0] * p[1] * p[2]
        lpda_sa += value
        listLPDA_sa.append(value)
    lpda_sa = lpda_sa/len(paretoPoints_sa)
    min_lpda_sa = min(listLPDA_sa)

    # LPDA = Latency * Power * Delay * Area
    lpda_bo = lpda_bo / 1e3
    lpda_ds = lpda_ds / 1e3
    lpda_ga = lpda_ga / 1e3
    lpda_sa = lpda_sa / 1e3

    # lpda_ref = power * perf * area
    # min_lpda_bo = min_lpda_bo / lpda_ref
    # min_lpda_ga = min_lpda_ga / lpda_ref
    # min_lpda_sa = min_lpda_sa / lpda_ref
    # min_lpda_ds = min_lpda_ds / lpda_ref
    print("")
    print("*" * 16 + " LPDA Comparison " + "*" * 16)
    print("MOTPE-F PDA: " + str(lpda_bo))
    print("MOTPE-D PDA: " + str(lpda_ds))
    print("NSGA PDA:    " + str(lpda_ga))
    print("SA PDA:      " + str(lpda_sa))

    # print("MINIMUM MOTPE-F PDA Normalized: " + str(min_lpda_bo))
    # print("MINIMUM NSGA PDA Normalized:    " + str(min_lpda_ga))
    # print("MINIMUM SA PDA Normalized:      " + str(min_lpda_sa))
    # print("MINIMUM MOTPE-D PDA Normalized: " + str(min_lpda_ds))

    # ADRS
    print("")
    print("*" * 16 + " ADRS Comparison " + "*" * 16)
    diff = 0.0
    for r in paretoPoints:
        dist = []
        for b in paretoPoints_bo:
            tmp = max(abs(b[0]-r[0])/r[0], abs(b[1]-r[1])/r[1], abs(b[2]-r[2])/r[2])
            dist.append(tmp)
        f = min(dist)
        diff += f
    adrs_bo = diff / len(paretoPoints)
    print("MOTPE-F ADRS: " + str(adrs_bo))

    diff = 0.0
    for r in paretoPoints:
        dist = []
        for s in paretoPoints_ds:
            tmp = max(abs(s[0] - r[0]) / r[0], abs(s[1] - r[1]) / r[1], abs(s[2] - r[2]) / r[2])
            dist.append(tmp)
        f = min(dist)
        diff += f
    adrs_ds = diff / len(paretoPoints)
    print("MOTPE-D ADRS: " + str(adrs_ds))

    diff = 0.0
    for r in paretoPoints:
        dist = []
        for g in paretoPoints_ga:
            tmp = max(abs(g[0] - r[0]) / r[0], abs(g[1] - r[1]) / r[1], abs(g[2] - r[2]) / r[2])
            dist.append(tmp)
        f = min(dist)
        diff += f
    adrs_ga = diff / len(paretoPoints)
    print("NSGA ADRS:    " + str(adrs_ga))

    diff = 0.0
    for r in paretoPoints:
        dist = []
        for s in paretoPoints_sa:
            tmp = max(abs(s[0] - r[0]) / r[0], abs(s[1] - r[1]) / r[1], abs(s[2] - r[2]) / r[2])
            dist.append(tmp)
        f = min(dist)
        diff += f
    adrs_sa = diff / len(paretoPoints)
    print("SA ADRS:      " + str(adrs_sa))
