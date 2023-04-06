# -*- coding: utf-8 -*-
# @Time : 2023/1/2 9:32
# @Author : hzkuang
# @Project : HLSDSE
# @File : hls_dse.py

import optuna
import argparse
import subprocess
from common import *
from sa import SimulatedAnnealingSampler
from hls_basic import HLSBasic
sys.path.append(".")


def floatParaSpace(trial, paraDict, fromVal: float = 0.0, toVal: float = 1.0):
    for key in paraDict:
        paraDict[key] = trial.suggest_float(key, fromVal, toVal)
    return paraDict


def discreteParaSpace(trial, paraDict, params):
    for key in paraDict:
        tag = key.split('_')[0]
        if tag == 'F':
            paraDict[key] = trial.suggest_categorical(key, params['inline'])
        elif tag == 'LU':
            paraDict[key] = trial.suggest_categorical(key, params['factor'])
        elif (tag == 'LP') or (tag == 'LF'):
            paraDict[key] = trial.suggest_categorical(key, params['state'])
        elif (tag == 'IPF') or (tag == 'IRF') or (tag == 'APF') or (tag == 'ARF'):
            paraDict[key] = trial.suggest_categorical(key, params['factor'])
        elif (tag == 'IPT') or (tag == 'IRT') or (tag == 'APT') or (tag == 'ART'):
            paraDict[key] = trial.suggest_categorical(key, params['arrtype'])
        elif tag == 'AST':
            paraDict[key] = trial.suggest_categorical(key, params['sttype'])
        elif tag == 'ASI':
            paraDict[key] = trial.suggest_categorical(key, params['stimpl'])
        elif tag == 'OPI':
            paraDict[key] = trial.suggest_categorical(key, params['opimpl']['int'])
        elif tag == 'FOPI':
            paraDict[key] = trial.suggest_categorical(key, params['opimpl']['float'])
        elif tag == 'DOPI':
            paraDict[key] = trial.suggest_categorical(key, params['opimpl']['double'])
        elif tag == 'HOPI':
            paraDict[key] = trial.suggest_categorical(key, params['opimpl']['half'])
        elif (tag == 'ASL') or (tag == 'OPL') or (tag == 'FOPL') or (tag == 'DOPL') or (tag == 'HOPL'):
            paraDict[key] = trial.suggest_categorical(key, params['latency'])
        else:
            print("[WARNING] No corresponding parameter type!!!")

    return paraDict


def objective(trial):
    global iterNum, basic
    # get the global variables from basic
    paraDict = basic.paraDict
    dataset_path = basic.dataset_path
    tempDir = basic.tempDir
    static_config = basic.static_config
    params = basic.params
    ori_prj_path = basic.ori_prj_path
    hls_temp = basic.hls_temp
    hls_script_path = basic.hls_script_path
    case = basic.case
    top = basic.top
    alg = basic.alg
    encode = basic.encode

    print("Initial paraDict:")
    print(paraDict)

    # suggest a group of params
    if encode == 'float':
        paraDict = floatParaSpace(trial, paraDict, fromVal=0.0, toVal=1.0)
        print("Float paraDict:")
        print(paraDict)
    else:
        paraDict = discreteParaSpace(trial, paraDict, params)
        print("Discrete paraDict:")
        print(paraDict)

    # generate tcl for HLS
    dir_json = os.path.join(hls_script_path, "dir_%d.json" % iterNum)
    dir_tcl = os.path.join(hls_script_path, "dir_%d.tcl" % iterNum)
    hls_tcl = os.path.join(hls_script_path, "hls_%d.tcl" % iterNum)
    genConfig(encode, params, static_config, paraDict, dir_tcl, tempDir, dir_json)
    f_script = open(hls_temp, "r")
    content = f_script.read()
    f_script.close()
    content = content.replace('dir_test.tcl', 'dir_%d.tcl' % iterNum)
    f_script = open(hls_tcl, "w")
    f_script.write(content)
    f_script.close()
    print("Running Vitis HLS and Vivado to get PPA...")
    p = subprocess.Popen('vitis_hls -f ' + hls_tcl, shell=True)
    try:
        p.wait(7200)
    except subprocess.TimeoutExpired:
        p.terminate()
        print("[INFO] Subprocess timeout !")
        with open('./runtime.log', 'a') as tlog:
            tlog.write(("Iteration: %d, Timeout !" % iterNum) + '\n')
    print("Collecting adb files, hls/syn/impl report and Verilog files...")
    rpt_list = get_adb_rpt_verilog(case, top, alg, ori_prj_path, dataset_path, iterNum)
    dictPPA = getPPA(rpt_list)
    ppa_rpt = os.path.join(hls_script_path, "ppa_%d.json" % iterNum)
    with open(ppa_rpt, "w") as fout:
        fout.write(json.dumps(dictPPA, indent=4))

    npower, nperf, narea = normalizePPA(params, dictPPA)
    if alg == 'sa':
        ppa = npower + nperf + narea
    else:
        ppa = [npower, nperf, narea]
    iterNum = iterNum + 1
    return ppa


def runDSE(basic):
    # specify the experiment name
    case = basic.case
    alg = basic.alg
    num = basic.num
    study_name = case + "_" + alg + "_dse"
    storage = "sqlite:///" + study_name + ".db"
    # specify random number seed
    seed = 128
    # choose the algorithm for DSE
    if alg == "sa":
        print("[INFO] Using Simulated Annealing for HLS DSE")
        sampler = SimulatedAnnealingSampler(seed=seed)
        study = optuna.create_study(storage=storage, study_name=study_name, sampler=sampler, direction="minimize",
                                    load_if_exists=True)
    else:
        if alg == "motpe":
            print("[INFO] Using MOTPE based Bayesian Optimization for HLS DSE")
            # hyperparameters of MOTPE
            n_startup_trials = 20
            n_ehvi_candidates = 24
            sampler = optuna.samplers.MOTPESampler(n_startup_trials=n_startup_trials,
                                                   n_ehvi_candidates=n_ehvi_candidates,
                                                   seed=seed)
        else:
            print("[INFO] Using NSGA-II for HLS DSE")
            sampler = optuna.samplers.NSGAIISampler(seed=seed)

        study = optuna.create_study(storage=storage, study_name=study_name, sampler=sampler,
                                    directions=["minimize", "minimize", "minimize"], load_if_exists=True)

    study.optimize(objective, n_trials=num, show_progress_bar=True)
    print("Number of finished trials: ", len(study.trials))

    if alg == "sa":
        optuna.visualization.plot_optimization_history(study)
        optuna.visualization.plot_parallel_coordinate(study)
        optuna.visualization.plot_param_importances(study)
        optuna.visualization.plot_contour(study)
        optuna.visualization.plot_slice(study)

        print("Best trial:")
        print("Value: ", study.best_trial.value)
        print("Params: ")
        for key, value in study.best_trial.params.items():
            print("{}: {}".format(key, value))
    else:
        print("Pareto front:")
        trials = sorted(study.best_trials, key=lambda t: t.values)
        for trial in trials:
            print("Trial#{}".format(trial.number))
            print("Params: {}".format(trial.params))

        # Visualization
        # Plot Patero-Front 3D figure
        fig_prt = optuna.visualization.plot_pareto_front(study, target_names=["power", "perf", "area"])
        fig_prt.show()
        print(f"Number of trials on the Pareto front: {len(study.best_trials)}")

        trial_with_lowest_power = min(study.best_trials, key=lambda t: t.values[0])
        print(f"Trial with lowest power: ")
        print(f"\tnumber: {trial_with_lowest_power.number}")
        print(f"\tparams: {trial_with_lowest_power.params}")
        print(f"\tvalues: {trial_with_lowest_power.values}")

        trial_with_best_cp = min(study.best_trials, key=lambda t: t.values[1])
        print(f"Trial with best performance: ")
        print(f"\tnumber: {trial_with_best_cp.number}")
        print(f"\tparams: {trial_with_best_cp.params}")
        print(f"\tvalues: {trial_with_best_cp.values}")

        trial_with_smallest_area = min(study.best_trials, key=lambda t: t.values[2])
        print(f"Trial with smallest area: ")
        print(f"\tnumber: {trial_with_smallest_area.number}")
        print(f"\tparams: {trial_with_smallest_area.params}")
        print(f"\tvalues: {trial_with_smallest_area.values}")

        fig_pwr_h = optuna.visualization.plot_optimization_history(study, target=lambda t: t.values[0], target_name="power")
        fig_perf_h = optuna.visualization.plot_optimization_history(study, target=lambda t: t.values[1], target_name="perf")
        fig_area_h = optuna.visualization.plot_optimization_history(study, target=lambda t: t.values[2], target_name="area")
        fig_pwr_h.show()
        fig_perf_h.show()
        fig_area_h.show()

        fig_pwr_i = optuna.visualization.plot_param_importances(study, target=lambda t: t.values[0], target_name="power")
        fig_perf_i = optuna.visualization.plot_param_importances(study, target=lambda t: t.values[1], target_name="perf")
        fig_area_i = optuna.visualization.plot_param_importances(study, target=lambda t: t.values[2], target_name="area")
        fig_pwr_i.show()
        fig_perf_i.show()
        fig_area_i.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HLS Design Space Exploration")
    parser.add_argument("--mode", type=str, help="The running mode of dse flow", default="opt")
    parser.add_argument("--bench", type=str, help="The public benchmark name.", default="MachSuite")
    parser.add_argument("--case", type=str, help="The name of the benchmark.", default="aes")
    parser.add_argument("--ver", type=str, help="The version of the benchmark.", default="aes")
    parser.add_argument("--num", type=int, help="The number of optimization iterations.", default=100)
    parser.add_argument("--alg", type=str, help="The DSE algorithm.", default="motpe")
    parser.add_argument("--device", type=str, help="FPGA device for implementation.", default="xc7vx485tffg1761-2")
    parser.add_argument("--clk", type=str, help="Clock period for implementation.", default="10")
    parser.add_argument("--encode", type=str, help="Float or discrete encoding style.", default="float")

    args = parser.parse_args()

    mode = args.mode
    bench = args.bench
    case = args.case
    ver = args.ver
    num = args.num
    alg = args.alg
    encode = args.encode

    root = os.path.abspath("../")
    basic = HLSBasic(root, mode, bench, case, ver, encode, num, alg)
    iterNum = 0

    runDSE(basic)

    print("[INFO] HLS Design Space Exploration is Done!")
    