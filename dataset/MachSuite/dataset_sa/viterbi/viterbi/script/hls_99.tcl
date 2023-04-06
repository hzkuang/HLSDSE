cd /mnt/sda1/code/HLSDSE_V2/benchmark/MachSuite/viterbi/viterbi
open_project viterbi_sa_prj
add_files viterbi.c
add_files local_support.c
set_top viterbi
open_solution -reset solution
set_part xc7vx485tffg1761-2
create_clock -period 10
source /mnt/sda1/code/HLSDSE_V2/dataset/MachSuite/sa_ds/viterbi/viterbi/script/dir_99.tcl
csynth_design
export_design -flow impl -rtl verilog -format ip_catalog
exit
