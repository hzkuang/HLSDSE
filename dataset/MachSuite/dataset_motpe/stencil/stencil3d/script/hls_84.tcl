cd ../benchmark/MachSuite/stencil/stencil3d

open_project stencil_prj

add_files stencil.c
add_files input.data
add_files check.data
add_files local_support.c

add_files -tb ../../common/support.c
add_files -tb ../../common/harness.c 

set_top stencil3d
open_solution -reset solution

set_part xc7vx485tffg1761-2
create_clock -period 10

source ../../../../dataset/stencil/stencil3d/dir_84.tcl

csynth_design
# cosim_design -rtl verilog -tool xsim
# set_param general.maxThreads 16
export_design -flow impl -rtl verilog -format ip_catalog

exit
