# -*- coding: utf-8 -*-
# @Time : 2023/1/2 9:46
# @Author : hzkuang
# @Project : HLSDSE
# @File : common.py

import os
import sys
import yaml
import json
import glob
import shutil
import numpy as np
from math import floor
from parse_xml import *
sys.path.append(".")

# Constant
F1: float = 1e8
F2: float = 1e8
F3: float = 1e8
F4: float = 1e8
WLUT: float = 0.3
WFF: float = 0.25
WDSP: float = 0.3
WBRAM: float = 0.05
WURAM: float = 0.05
WSRL: float = 0.05


def basicOption():
    return {
        "INLINE": {"-off": [], "-recursive": []},
        "PIPELINE": {"-style": []},
        "UNROLL": {"-factor": []},
        "PARTITION": {"-factor": [], "-type": []},
        "RESHAPE": {"-factor": [], "-type": []},
        "STORAGE": {"-type": [], "-impl": [], "-latency": []},
    }


def createFolder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def getYaml(yaml_file):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    print(file_data)
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    return data


def genConfig(encode, params, static_config, paraDict, dir_tcl, tempDir, dir_json):

    funcList = static_config["funcList"]
    loopList = static_config["loopList"]
    arrList = static_config["arrList"]
    interList = static_config["interList"]
    dictOp = static_config["dictOp"]

    if encode == 'float':
        print("[INFO] Using float encoding method!")
        inline = params['inline']
        factor = params['factor']
        arrtype = params['arrtype']
        opimpl = params['opimpl']
        sttype = params['sttype']
        stimpl = params['stimpl']
        latency = params['latency']
        state = params['state']

        # Convert numerical values to actual options
        for key in paraDict:
            name = key.split('_')[0]
            if name == 'F':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(inline))
                paraDict[key] = inline[idx]
            elif name == 'LU':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(factor))
                paraDict[key] = factor[idx]
            elif name == 'LP':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(state))
                paraDict[key] = state[idx]
            elif name == 'LF':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(state))
                paraDict[key] = state[idx]
            elif name == 'APF':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(factor))
                paraDict[key] = factor[idx]
            elif name == 'APT':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(arrtype))
                paraDict[key] = arrtype[idx]
            elif name == 'ARF':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(factor))
                paraDict[key] = factor[idx]
            elif name == 'ART':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(arrtype))
                paraDict[key] = arrtype[idx]
            elif name == 'AST':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(sttype))
                paraDict[key] = sttype[idx]
            elif name == 'ASI':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(stimpl))
                paraDict[key] = stimpl[idx]
            elif name == 'ASL':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(latency))
                paraDict[key] = latency[idx]
            elif name == 'IPF':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(factor))
                paraDict[key] = factor[idx]
            elif name == 'IPT':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(arrtype))
                paraDict[key] = arrtype[idx]
            elif name == 'IRF':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(factor))
                paraDict[key] = factor[idx]
            elif name == 'IRT':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(arrtype))
                paraDict[key] = arrtype[idx]
            elif name == 'OPI':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(opimpl['int']))
                paraDict[key] = opimpl['int'][idx]
            elif name == 'OPL':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(latency))
                paraDict[key] = latency[idx]
            elif name == 'FOPI':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(opimpl['float']))
                paraDict[key] = opimpl['float'][idx]
            elif name == 'FOPL':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(latency))
                paraDict[key] = latency[idx]
            elif name == 'DOPI':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(opimpl['double']))
                paraDict[key] = opimpl['double'][idx]
            elif name == 'DOPL':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(latency))
                paraDict[key] = latency[idx]
            elif name == 'HOPI':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(opimpl['half']))
                paraDict[key] = opimpl['half'][idx]
            elif name == 'HOPL':
                var = paraDict[key]
                assert var < 1.0, "Param value is not less than 1 !"
                idx = floor(var * len(latency))
                paraDict[key] = latency[idx]

    else:
        print("[INFO] Using discrete encoding method!")

    # Fill the blanks in dir.json and generate dir.tcl for HLS
    print("[INFO] Generating Vitis HLS directive.tcl file...")
    cntF = cntL = cntA = cntI = cntO = 0
    fileDir = open(dir_tcl, 'w')

    for func in funcList:
        if func is None:
            break
        else:
            tempDir["Function"][func]["INLINE"] = paraDict['F_' + str(cntF)]
            if (paraDict['F_' + str(cntF)] == '-on') == 0:
                tcl = "set_directive_inline " + paraDict['F_' + str(cntF)] + " " + func
                fileDir.write(tcl + "\n")
            else:
                tcl = "set_directive_inline " + func
                fileDir.write(tcl + "\n")
            cntF = cntF + 1

    for group in loopList:
        ppl_flag = 0
        if group is None:
            break
        else:
            for loop in loopList[group]['level']:
                if ppl_flag == 0:
                    if loop in loopList[group]['flatten']:
                        tempDir["Loop"][group][loop]["FLATTEN"]["-state"] = paraDict['LF_' + str(cntL)]
                        if paraDict['LF_' + str(cntL)] == '-on':
                            tcl = "set_directive_loop_flatten " + loop
                            fileDir.write(tcl + "\n")
                            cntL = cntL + 1
                            continue
                        else:
                            tcl = "set_directive_loop_flatten -off " + loop
                            fileDir.write(tcl + "\n")
                    if loop in loopList[group]['unroll']:
                        tempDir["Loop"][group][loop]["UNROLL"]["-factor"] = paraDict['LU_' + str(cntL)]
                        if paraDict['LU_' + str(cntL)] > 0:
                            tcl = "set_directive_unroll -factor " + str(paraDict['LU_' + str(cntL)]) + " " + loop
                            fileDir.write(tcl + "\n")
                    if loop in loopList[group]['pipeline']:
                        tempDir["Loop"][group][loop]["PIPELINE"]["-style"] = 'stp'
                        tempDir["Loop"][group][loop]["PIPELINE"]["-state"] = paraDict['LP_' + str(cntL)]
                        if paraDict['LP_' + str(cntL)] == '-on':
                            tcl = "set_directive_pipeline -style stp " + loop
                            fileDir.write(tcl + "\n")
                            ppl_flag = 1
                        else:
                            tcl = "set_directive_pipeline -off " + loop
                            fileDir.write(tcl + "\n")
                cntL = cntL + 1

    for arr in arrList:
        if arr is None:
            break
        else:
            tempDir["Array"][arr]["PARTITION"]["-factor"] = paraDict['APF_' + str(cntA)]
            tempDir["Array"][arr]["PARTITION"]["-type"] = paraDict['APT_' + str(cntA)]
            tempDir["Array"][arr]["RESHAPE"]["-factor"] = paraDict['ARF_' + str(cntA)]
            tempDir["Array"][arr]["RESHAPE"]["-type"] = paraDict['ART_' + str(cntA)]
            tempDir["Array"][arr]["STORAGE"]["-type"] = paraDict['AST_' + str(cntA)]
            tempDir["Array"][arr]["STORAGE"]["-impl"] = paraDict['ASI_' + str(cntA)]
            tempDir["Array"][arr]["STORAGE"]["-latency"] = paraDict['ASL_' + str(cntA)]
            if paraDict['APF_' + str(cntA)] > 0:
                tcl = "set_directive_array_partition -factor " + str(paraDict['APF_' + str(cntA)]) + " -type " + \
                      paraDict['APT_' + str(cntA)] + " " + arr
                fileDir.write(tcl + "\n")
            if paraDict['ARF_' + str(cntA)] > 0:
                tcl = "set_directive_array_reshape -factor " + str(paraDict['ARF_' + str(cntA)]) + " -type " + paraDict[
                    'ART_' + str(cntA)] + " " + arr
                fileDir.write(tcl + "\n")
            tcl = "set_directive_bind_storage -type " + paraDict['AST_' + str(cntA)] + " -impl " + paraDict[
                'ASI_' + str(cntA)] + " -latency " + str(paraDict['ASL_' + str(cntA)]) + " " + arr
            fileDir.write(tcl + "\n")
            cntA = cntA + 1

    for inter in interList:
        if inter is None:
            break
        else:
            tempDir["Interface"][inter]["PARTITION"]["-factor"] = paraDict['IPF_' + str(cntI)]
            tempDir["Interface"][inter]["PARTITION"]["-type"] = paraDict['IPT_' + str(cntI)]
            tempDir["Interface"][inter]["RESHAPE"]["-factor"] = paraDict['IRF_' + str(cntI)]
            tempDir["Interface"][inter]["RESHAPE"]["-type"] = paraDict['IRT_' + str(cntI)]
            if paraDict['IPF_' + str(cntI)] > 0:
                tcl = "set_directive_array_partition -factor " + str(paraDict['IPF_' + str(cntI)]) + " -type " + \
                      paraDict['IPT_' + str(cntI)] + " " + inter
                fileDir.write(tcl + "\n")
            if paraDict['IRF_' + str(cntI)] > 0:
                tcl = "set_directive_array_reshape -factor " + str(paraDict['IRF_' + str(cntI)]) + " -type " + paraDict[
                    'IRT_' + str(cntI)] + " " + inter
                fileDir.write(tcl + "\n")
            cntI = cntI + 1

    for optype in dictOp:
        for key in dictOp[optype]:
            if key is None:
                break
            else:
                opList = dictOp[optype][key]
                for op in opList:
                    if op is None:
                        break
                    else:
                        if optype == 'int':
                            tempDir["Operation"][key][op]["-impl"] = paraDict['OPI_' + str(cntO)]
                            tempDir["Operation"][key][op]["-latency"] = paraDict['OPL_' + str(cntO)]
                            tcl = "set_directive_bind_op -op " + op + " -impl " + paraDict[
                                'OPI_' + str(cntO)] + " -latency " + str(paraDict['OPL_' + str(cntO)]) + " " + key
                            fileDir.write(tcl + "\n")
                        elif optype == 'float':
                            tempDir["Operation"][key][op]["-impl"] = paraDict['FOPI_' + str(cntO)]
                            tempDir["Operation"][key][op]["-latency"] = paraDict['FOPL_' + str(cntO)]
                            tcl = "set_directive_bind_op -op " + op + " -impl " + paraDict[
                                'FOPI_' + str(cntO)] + " -latency " + str(paraDict['FOPL_' + str(cntO)]) + " " + key
                            fileDir.write(tcl + "\n")
                        elif optype == 'double':
                            tempDir["Operation"][key][op]["-impl"] = paraDict['DOPI_' + str(cntO)]
                            tempDir["Operation"][key][op]["-latency"] = paraDict['DOPL_' + str(cntO)]
                            tcl = "set_directive_bind_op -op " + op + " -impl " + paraDict[
                                'DOPI_' + str(cntO)] + " -latency " + str(paraDict['DOPL_' + str(cntO)]) + " " + key
                            fileDir.write(tcl + "\n")
                        elif optype == 'half':
                            tempDir["Operation"][key][op]["-impl"] = paraDict['HOPI_' + str(cntO)]
                            tempDir["Operation"][key][op]["-latency"] = paraDict['HOPL_' + str(cntO)]
                            tcl = "set_directive_bind_op -op " + op + " -impl " + paraDict[
                                'HOPI_' + str(cntO)] + " -latency " + str(paraDict['HOPL_' + str(cntO)]) + " " + key
                            fileDir.write(tcl + "\n")
                        cntO = cntO + 1

    fileDir.close()

    with open(dir_json, "w") as fout:
        fout.write(json.dumps(tempDir, indent=4))

    print("[INFO] Successfully generated Vitis HLS directive.tcl and hls.tcl files !")


def getPPA(rpt_list):
    dictPPA = {}
    hls_rpt = rpt_list[0]
    hls_xml = rpt_list[1]
    syn_rpt = rpt_list[2]
    impl_rpt = rpt_list[3]
    power_rpt = rpt_list[4]

    LATENCY = F4
    dictLatency = {}
    if os.path.exists(hls_xml):
        print("[INFO] Reading Latency Information...")
        xml_parser = read_xml(hls_xml)
        root = get_xml_root(xml_parser)
        perf_info = find_first_node(root, 'PerformanceEstimates')
        latency_info = find_first_node(perf_info, 'SummaryOfOverallLatency')

        if latency_info.find('Best-caseLatency').text != 'undef':
            dictLatency['best_latency'] = int(latency_info.find('Best-caseLatency').text)
            dictLatency['worst_latency'] = int(latency_info.find('Worst-caseLatency').text)
            dictLatency['average_latency'] = int(latency_info.find('Average-caseLatency').text)
            dictLatency['best_time_latency'] = latency_info.find('Best-caseRealTimeLatency').text
            dictLatency['worst_time_latency'] = latency_info.find('Worst-caseRealTimeLatency').text
            dictLatency['average_time_latency'] = latency_info.find('Average-caseRealTimeLatency').text
            dictLatency['min_interval'] = int(latency_info.find('Interval-min').text)
            dictLatency['max_interval'] = int(latency_info.find('Interval-max').text)
            dictLatency['Latency'] = dictLatency['average_latency']
        else:
            dictLatency['Latency'] = 1000
    else:
        dictLatency['Latency'] = LATENCY
    print(dictLatency)
    dictPPA['LATENCY'] = dictLatency

    LUT = FF = DSP = BRAM = URAM = F1
    CP = F2
    if os.path.exists(hls_rpt):
        print("[INFO] Reading HLS Prediction report...")
        f_hls = open(hls_rpt, 'r')
        for line in f_hls.readlines():
            if line.startswith('|Total'):
                res = [i for i in line.split('|')]
                BRAM = int(res[2].strip())
                DSP = int(res[3].strip())
                FF = int(res[4].strip())
                LUT = int(res[5].strip())
                URAM = int(res[6].strip())
            elif line.startswith('    |ap_clk  |'):
                res = [i for i in line.split()]
                CP = float(res[-4])
    else:
        print("[INFO] HLS Flow Faild !")
    dictPPA['HLS'] = {'LUT': LUT, 'FF': FF, 'DSP': DSP, 'BRAM': BRAM, 'URAM': URAM, 'CP': CP}
    print("HLS Prediction Results:")
    print("LUT = %d, FF = %d, DSP = %d, BRAM = %d, URAM = %d, CP = %f" % (LUT, FF, DSP, BRAM, URAM, CP))

    LUT = FF = DSP = BRAM = URAM = SRL = F1
    CP = F2
    if os.path.exists(syn_rpt):
        print("[INFO] Reading RTL Synthesis report...")
        f_syn = open(syn_rpt, 'r')
        for line in f_syn.readlines():
            res = [i for i in line.split() if i.isdigit()]
            if line.startswith('LUT'):
                LUT = int(res[0])
            elif line.startswith('FF'):
                FF = int(res[0])
            elif line.startswith('DSP'):
                DSP = int(res[0])
            elif line.startswith('BRAM'):
                BRAM = int(res[0])
            elif line.startswith('URAM'):
                URAM = int(res[0])
            elif line.startswith('SRL'):
                SRL = int(res[0])
            elif line.startswith('| Post-Route |'):
                res = [i for i in line.split()]
                CP = float(res[-2])
    else:
        print("[INFO] Synthesis Flow Faild !")
    dictPPA['SYN'] = {'LUT': LUT, 'FF': FF, 'DSP': DSP, 'BRAM': BRAM, 'URAM': URAM, 'SRL': SRL, 'CP': CP}
    print("RTL Synthesis Results:")
    print("LUT = %d, FF = %d, DSP = %d, BRAM = %d, URAM = %d, SRL = %d, CP = %f" % (LUT, FF, DSP, BRAM, URAM, SRL, CP))

    LUT = FF = DSP = BRAM = URAM = SRL = F1
    CP = F2
    PWR = F3
    if os.path.exists(impl_rpt):
        print("[INFO] Reading post-implementation report...")
        f_impl = open(impl_rpt, 'r')
        for line in f_impl.readlines():
            res = [i for i in line.split() if i.isdigit()]
            if line.startswith('LUT'):
                LUT = int(res[0])
            elif line.startswith('FF'):
                FF = int(res[0])
            elif line.startswith('DSP'):
                DSP = int(res[0])
            elif line.startswith('BRAM'):
                BRAM = int(res[0])
            elif line.startswith('URAM'):
                URAM = int(res[0])
            elif line.startswith('SRL'):
                SRL = int(res[0])
            elif line.startswith('CP achieved post-implementation'):
                res = [i for i in line.split()]
                CP = float(res[-1])
    if os.path.exists(power_rpt):
        f_power = open(power_rpt, 'r')
        for line in f_power.readlines():
            if line.startswith("| Total On-Chip Power (W)  |"):
                res = [i for i in line.split()]
                PWR = float(res[-2])
                break
    else:
        print("Implementation Flow Failed !")
    dictPPA['IMPL'] = {'LUT': LUT, 'FF': FF, 'DSP': DSP, 'BRAM': BRAM, 'URAM': URAM, 'SRL': SRL, 'CP': CP, 'PWR': PWR}
    print("Post-Implementation Results:")
    print("LUT = %d, FF = %d, DSP = %d, BRAM = %d, URAM = %d, SRL = %d, CP = %f, PWR = %f" % (LUT, FF, DSP, BRAM, URAM,
                                                                                              SRL, CP, PWR))
    return dictPPA


def normalizePPA(params, dictPPA):
    wght = [WLUT, WFF, WDSP, WBRAM, WURAM, WSRL]
    POW = float(params["POW"][0])
    CLK = float(params["CLK"][0])
    LTC = float(params["LATENCY"][0])
    RU = [float(params["LUT"][0]), float(params["FF"][0]), float(params["DSP"][0]), float(params["BRAM"][0]),
          float(params["URAM"][0]), float(params["SRL"][0])]
    NUM = sum(np.multiply(wght, RU))
    power = dictPPA['IMPL']['PWR']
    cp = dictPPA['IMPL']['CP']
    lat = dictPPA['LATENCY']['Latency']
    perf = cp * lat
    usg = [dictPPA['IMPL']['LUT'], dictPPA['IMPL']['FF'], dictPPA['IMPL']['DSP'], dictPPA['IMPL']['BRAM'],
           dictPPA['IMPL']['URAM'], dictPPA['IMPL']['SRL']]
    area = sum(np.multiply(wght, usg))
    # normalize ppa
    npower = power / POW
    nperf = perf / (CLK * LTC)
    narea = area / NUM
    return npower, nperf, narea


def get_adb_rpt_verilog(case, top, alg, ori_prj_path, dataset_path, iterNum):
    ir_path = case + '_' + alg + '_prj/solution/.autopilot/db/'
    prj_path = os.path.join(dataset_path, 'prj_%d' % iterNum)
    createFolder(prj_path)
    graph_path = os.path.join(prj_path, 'graph')
    report_path = os.path.join(prj_path, 'report')
    verilog_path = os.path.join(prj_path, 'verilog')
    createFolder(graph_path)
    createFolder(report_path)
    createFolder(verilog_path)

    for adb_file in glob.glob(os.path.join(ori_prj_path, ir_path) + '*.adb'):
        if 'bind' not in adb_file and 'sched' not in adb_file:
            func_name = (adb_file.split('/')[-1]).split('.')[0]
            adb_path_ori = os.path.join(ori_prj_path, ir_path + func_name + '.adb')
            adb_xml_path_ori = os.path.join(ori_prj_path, ir_path + func_name + '.adb.xml')
            shutil.copy(adb_path_ori, graph_path)
            shutil.copy(adb_xml_path_ori, graph_path)

    # copy ll and bc files
    bc_path = os.path.join(ori_prj_path, ir_path, 'a.o.3.bc')
    ll_path = os.path.join(ori_prj_path, ir_path, 'apatb_' + top + '_ir.ll')
    if os.path.exists(bc_path):
        shutil.copy(bc_path, graph_path)
    if os.path.exists(ll_path):
        shutil.copy(ll_path, graph_path)

    # copy hls reports
    verbose_rpt = os.path.join(ori_prj_path, ir_path, top + '.verbose.rpt')
    verbose_xml = verbose_rpt + '.xml'
    csyn_path = case + '_' + alg + '_prj/solution/syn/report'
    hls_rpt = os.path.join(ori_prj_path, csyn_path, top + '_csynth.rpt')
    hls_xml = os.path.join(ori_prj_path, csyn_path, top + '_csynth.xml')
    hls_rpt_full = os.path.join(ori_prj_path, csyn_path, 'csynth.rpt')
    hls_xml_full = os.path.join(ori_prj_path, csyn_path, 'csynth.xml')
    solution_path = case + '_' + alg + '_prj/solution'
    directive_record = os.path.join(ori_prj_path, solution_path, 'solution.directive')
    solution_log = os.path.join(ori_prj_path, solution_path, 'solution.log')
    solution_data = os.path.join(ori_prj_path, solution_path, 'solution_data.json')
    hls_rpt_list = [verbose_rpt, verbose_xml, hls_rpt, hls_xml, hls_rpt_full, hls_xml_full, directive_record,
                    solution_log, solution_data]
    for hls_idx in hls_rpt_list:
        if os.path.exists(hls_idx):
            shutil.copy(hls_idx, report_path)

    # copy Verilog files
    verilog_folder = ''.join([case, '_', alg, '_prj/solution/syn/verilog'])
    ori_verilog_path = os.path.join(ori_prj_path, verilog_folder)
    if os.path.exists(ori_verilog_path):
        veri_list = os.listdir(ori_verilog_path)
        for veri_idx in veri_list:
            veri_src = os.path.join(ori_verilog_path, veri_idx)
            shutil.copy(veri_src, verilog_path)
    else:
        with open('./hlsrun.log', 'a') as hlog:
            hlog.write(("Iteration: %d, HLS process failed !" % iterNum) + '\n')

    # copy syn/impl reports
    syn_rpt = os.path.join(ori_prj_path, case + '_' + alg + "_prj/solution/impl/report/verilog/export_syn.rpt")
    syn_xml = os.path.join(ori_prj_path, case + '_' + alg + "_prj/solution/impl/report/verilog/export_syn.xml")
    impl_rpt = os.path.join(ori_prj_path, case + '_' + alg + "_prj/solution/impl/report/verilog/export_impl.rpt")
    impl_xml = os.path.join(ori_prj_path, case + '_' + alg + "_prj/solution/impl/report/verilog/export_impl.xml")
    simple_impl_rpt = os.path.join(ori_prj_path, case + '_' + alg + "_prj/solution/impl/report/verilog/" + top +
                                   "_export.rpt")
    power_rpt = os.path.join(ori_prj_path, case + '_' + alg +
                             "_prj/solution/impl/verilog/project.runs/impl_1/bd_0_wrapper_power_routed.rpt")
    impl_rpt_list = [syn_rpt, syn_xml, impl_rpt, impl_xml, simple_impl_rpt, power_rpt]
    for impl_idx in impl_rpt_list:
        if os.path.exists(impl_idx):
            shutil.copy(impl_idx, report_path)

    rpt_list = [hls_rpt, hls_xml, syn_rpt, simple_impl_rpt, power_rpt]
    return rpt_list
