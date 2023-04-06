cd /mnt/sda1/code/HLSDSE_V2/benchmark/MachSuite/gemm/ncubed
open_project gemm_sa_prj
add_files gemm.c
add_files local_support.c
set_top gemm
open_solution -reset solution
set_part xc7vx485tffg1761-2
create_clock -period 10
source /mnt/sda1/code/HLSDSE_V2/dataset/MachSuite/sa_ds/gemm/ncubed/script/dir_22.tcl
csynth_design
export_design -flow impl -rtl verilog -format ip_catalog
exit
