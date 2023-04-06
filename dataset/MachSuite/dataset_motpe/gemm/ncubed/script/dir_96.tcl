set_directive_loop_flatten gemm/outer
set_directive_pipeline -off gemm/middle
set_directive_unroll -factor 2 gemm/inner
set_directive_pipeline -off gemm/inner
set_directive_array_reshape -factor 2 -type block gemm prod
set_directive_bind_op -op add -impl dsp -latency -1 gemm/outer i
set_directive_bind_op -op add -impl dsp -latency -1 gemm/middle j
set_directive_bind_op -op mul -impl fabric -latency -1 gemm/middle i_col
set_directive_bind_op -op add -impl fabric -latency -1 gemm/inner k
set_directive_bind_op -op mul -impl dsp -latency -1 gemm/inner k_col
set_directive_bind_op -op dadd -impl fabric -latency -1 gemm/inner sum
set_directive_bind_op -op dmul -impl fulldsp -latency -1 gemm/inner mult
