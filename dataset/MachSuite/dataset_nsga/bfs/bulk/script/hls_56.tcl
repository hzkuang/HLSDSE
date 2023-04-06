cd /mnt/sda1/code/HLSDSE_V2/benchmark/MachSuite/bfs/bulk
open_project bfs_nsga_prj
add_files bfs.c
add_files local_support.c
set_top bfs
open_solution -reset solution
set_part xc7vx485tffg1761-2
create_clock -period 10
source /mnt/sda1/code/HLSDSE_V2/dataset/MachSuite/nsga_ds/bfs/bulk/script/dir_56.tcl
csynth_design
export_design -flow impl -rtl verilog -format ip_catalog
exit
