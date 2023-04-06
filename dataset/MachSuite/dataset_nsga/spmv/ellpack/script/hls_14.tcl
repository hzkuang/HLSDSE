cd /mnt/sda1/code/HLSDSE_V2/benchmark/MachSuite/spmv/ellpack
open_project spmv_nsga_prj
add_files spmv.c
add_files local_support.c
set_top ellpack
open_solution -reset solution
set_part xc7vx485tffg1761-2
create_clock -period 10
source /mnt/sda1/code/HLSDSE_V2/dataset/MachSuite/nsga_ds/spmv/ellpack/script/dir_14.tcl
csynth_design
export_design -flow impl -rtl verilog -format ip_catalog
exit
