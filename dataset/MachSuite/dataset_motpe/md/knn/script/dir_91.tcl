set_directive_pipeline -off md_kernel/loop_i
set_directive_pipeline -style stp md_kernel/loop_j
set_directive_array_reshape -factor 2 -type block md_kernel force_x
set_directive_array_reshape -factor 2 -type cyclic md_kernel force_z
set_directive_array_partition -factor 2 -type block md_kernel position_x
set_directive_array_partition -factor 2 -type cyclic md_kernel position_y
set_directive_array_partition -factor 2 -type block md_kernel position_z
set_directive_bind_op -op dsub -impl fabric -latency -1 md_kernel/loop_j delx
set_directive_bind_op -op dsub -impl fabric -latency -1 md_kernel/loop_j dely
set_directive_bind_op -op dsub -impl fulldsp -latency -1 md_kernel/loop_j delz
set_directive_bind_op -op dmul -impl fulldsp -latency -1 md_kernel/loop_j r2inv
set_directive_bind_op -op dmul -impl fulldsp -latency -1 md_kernel/loop_j r6inv
set_directive_bind_op -op dmul -impl fulldsp -latency -1 md_kernel/loop_j potential
set_directive_bind_op -op dmul -impl fulldsp -latency -1 md_kernel/loop_j fx
set_directive_bind_op -op dmul -impl fulldsp -latency -1 md_kernel/loop_j fy
set_directive_bind_op -op dmul -impl fabric -latency -1 md_kernel/loop_j fz
