cd /mnt/sda1/code/HLSDSE_V2/benchmark/MachSuite/stencil/stencil3d
open_project stencil_motpe_prj
add_files stencil.c
add_files local_support.c
set_top stencil3d
open_solution -reset solution
set_part xc7vx485tffg1761-2
create_clock -period 10
source /mnt/sda1/code/HLSDSE_V2/dataset/MachSuite/motpe_ds/stencil/stencil3d/script/dir_24.tcl
csynth_design
export_design -flow impl -rtl verilog -format ip_catalog
exit
