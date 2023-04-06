cd /mnt/sda1/code/HLSDSE_V2/benchmark/MachSuite/fft/strided
open_project fft_motpe_prj
add_files fft.c
add_files local_support.c
set_top fft
open_solution -reset solution
set_part xc7vx485tffg1761-2
create_clock -period 10
source /mnt/sda1/code/HLSDSE_V2/dataset/MachSuite/motpe_ds/fft/strided/script/dir_56.tcl
csynth_design
export_design -flow impl -rtl verilog -format ip_catalog
exit
