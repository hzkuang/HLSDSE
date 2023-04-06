cd ../benchmark/MachSuite/nw/nw

open_project nw_prj

add_files nw.c
add_files input.data
add_files check.data
add_files local_support.c

add_files -tb ../../common/support.c
add_files -tb ../../common/harness.c 

set_top needwun
open_solution -reset solution

set_part xc7vx485tffg1761-2
create_clock -period 10

source ../../../../dataset/nw/nw/dir_15.tcl

csynth_design
# cosim_design -rtl verilog -tool xsim
# set_param general.maxThreads 16
export_design -flow impl -rtl verilog -format ip_catalog

exit
