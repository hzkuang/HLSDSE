cd /mnt/sda1/code/HLSDSE_V2/benchmark/MachSuite/md/knn
open_project md_sa_prj
add_files md.c
add_files local_support.c
set_top md_kernel
open_solution -reset solution
set_part xc7vx485tffg1761-2
create_clock -period 10
source /mnt/sda1/code/HLSDSE_V2/dataset/MachSuite/sa_ds/md/knn/script/dir_12.tcl
csynth_design
export_design -flow impl -rtl verilog -format ip_catalog
exit
