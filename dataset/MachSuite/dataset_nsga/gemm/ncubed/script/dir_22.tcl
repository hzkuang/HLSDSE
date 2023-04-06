set_directive_loop_flatten -off gemm/outer
set_directive_unroll -factor 2 gemm/outer
set_directive_unroll -factor 2 gemm/middle
set_directive_pipeline -style stp gemm/middle
set_directive_array_partition -factor 2 -type cyclic gemm m1
set_directive_array_partition -factor 2 -type cyclic gemm m2
set_directive_array_reshape -factor 2 -type cyclic gemm prod
set_directive_bind_op -op add -impl fabric -latency -1 gemm/outer i
set_directive_bind_op -op add -impl dsp -latency -1 gemm/middle j
set_directive_bind_op -op mul -impl dsp -latency -1 gemm/middle i_col
set_directive_bind_op -op add -impl dsp -latency -1 gemm/inner k
set_directive_bind_op -op mul -impl dsp -latency -1 gemm/inner k_col
set_directive_bind_op -op dadd -impl fulldsp -latency -1 gemm/inner sum
set_directive_bind_op -op dmul -impl fulldsp -latency -1 gemm/inner mult
