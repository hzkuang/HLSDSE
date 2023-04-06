cd /mnt/sda1/code/HLSDSE_V2/benchmark/MachSuite/aes/aes
open_project aes_sa_prj
add_files aes.c
add_files local_support.c
set_top aes256_encrypt_ecb
open_solution -reset solution
set_part xc7vx485tffg1761-2
create_clock -period 10
source /mnt/sda1/code/HLSDSE_V2/dataset/MachSuite/sa_ds/aes/aes/script/dir_2.tcl
csynth_design
export_design -flow impl -rtl verilog -format ip_catalog
exit
