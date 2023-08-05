# HLSDSE

## Prerequisites
- Optuna 3.1.0
- Vitis HLS 2022.1
- Vivado 2022.1

## Configure Design Space
- config.yaml
- params.yaml

The config.yaml and params.yaml under config folder are used to construct the HLS design space. 
We provide the corresponding yaml files for MachSuite benchmark used in paper. 
For new benchmark, users can write yaml files according to the rules described in our paper.

## Encoding Methods
- Float encoding
- Discrete encoding

MOTPE with float (discrete) encoding is denoted as MOTPE-F (MOTPE-D)

## Run HLS Design Space Exploration
```
cd flow
python3 hls_dse.py --case aes --ver aes
```
When running the above command, MOTPE with float encoding is used as default to explore the design space of *aes*.
The samples during DSE process are saved to path "./dse_ds/MachSuite/***_ds/". 
The paper results are in path "./dataset/MachSuite/".

If you want to change the DSE algorithm or the encoding method, add the following arguments:
- --alg [options: motpe, nsga, sa]
- --encode [options: float, discrete]

Besides, the constraint clock period and the target FPGA device can be specified by arguments:
- --clk
- --device

## Meta-Heuristics
- Simulated Annealing (SA)
- NSGA-II (based on Optuna)

These two algorithms are for comparison with our MOTPE-F.

## Publication
- [ISEDA'23] Multi-objective Design Space Exploration for High-Level Synthesis via Bayesian Optimization

## Contact
- If there is any question, please email to hzkuang22@m.fudan.edu.cn
- If you find HLSDSE useful, please cite our paper.
