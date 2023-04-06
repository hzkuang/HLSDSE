set_directive_inline init
set_directive_inline hist
set_directive_inline -off local_scan
set_directive_inline sum_scan
set_directive_inline -recursive last_step_scan
set_directive_inline -off update
set_directive_pipeline -style stp init/init_1
set_directive_unroll -factor 2 sum_scan/sum_1
set_directive_pipeline -off sum_scan/sum_1
set_directive_loop_flatten -off local_scan/local_1
set_directive_unroll -factor 2 local_scan/local_1
set_directive_pipeline -style stp local_scan/local_1
set_directive_loop_flatten last_step_scan/last_1
set_directive_pipeline -off last_step_scan/last_2
set_directive_loop_flatten -off hist/hist_1
set_directive_pipeline -style stp hist/hist_1
set_directive_loop_flatten -off update/update_1
set_directive_unroll -factor 2 update/update_1
set_directive_pipeline -off update/update_1
set_directive_pipeline -off update/update_2
set_directive_array_partition -factor 2 -type block ss_sort a
set_directive_array_reshape -factor 2 -type cyclic ss_sort a
set_directive_bind_op -op add -impl fabric -latency -1 ss_sort/sort_1 exp
set_directive_bind_op -op add -impl fabric -latency -1 init/init_1 i
set_directive_bind_op -op add -impl dsp -latency -1 hist/hist_1 blockID
set_directive_bind_op -op add -impl dsp -latency -1 hist/hist_2 i
set_directive_bind_op -op mul -impl dsp -latency -1 hist/hist_2 bucket_indx
set_directive_bind_op -op mul -impl dsp -latency -1 hist/hist_2 a_indx
set_directive_bind_op -op add -impl fabric -latency -1 local_scan/local_1 radixID
set_directive_bind_op -op add -impl fabric -latency -1 local_scan/local_2 i
set_directive_bind_op -op mul -impl dsp -latency -1 local_scan/local_2 bucket_indx
set_directive_bind_op -op add -impl dsp -latency -1 sum_scan/sum_1 radixID
set_directive_bind_op -op mul -impl dsp -latency -1 sum_scan/sum_1 bucket_indx
set_directive_bind_op -op add -impl dsp -latency -1 last_step_scan/last_1 radixID
set_directive_bind_op -op add -impl fabric -latency -1 last_step_scan/last_2 i
set_directive_bind_op -op mul -impl dsp -latency -1 last_step_scan/last_2 bucket_indx
set_directive_bind_op -op add -impl fabric -latency -1 update/update_1 blockID
set_directive_bind_op -op mul -impl fabric -latency -1 update/update_2 bucket_indx
set_directive_bind_op -op add -impl dsp -latency -1 update/update_2 i
set_directive_bind_op -op mul -impl dsp -latency -1 update/update_2 a_indx
