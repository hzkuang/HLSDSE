set_directive_inline -recursive init
set_directive_inline hist
set_directive_inline -recursive local_scan
set_directive_inline -off sum_scan
set_directive_inline last_step_scan
set_directive_inline -recursive update
set_directive_pipeline -style stp init/init_1
set_directive_pipeline -off sum_scan/sum_1
set_directive_loop_flatten local_scan/local_1
set_directive_pipeline -style stp local_scan/local_2
set_directive_loop_flatten last_step_scan/last_1
set_directive_unroll -factor 2 last_step_scan/last_2
set_directive_pipeline -style stp last_step_scan/last_2
set_directive_loop_flatten hist/hist_1
set_directive_pipeline -style stp hist/hist_2
set_directive_loop_flatten -off update/update_1
set_directive_unroll -factor 2 update/update_1
set_directive_pipeline -style stp update/update_1
set_directive_array_partition -factor 2 -type block ss_sort sum
set_directive_bind_op -op add -impl dsp -latency -1 ss_sort/sort_1 exp
set_directive_bind_op -op add -impl fabric -latency -1 init/init_1 i
set_directive_bind_op -op add -impl dsp -latency -1 hist/hist_1 blockID
set_directive_bind_op -op add -impl fabric -latency -1 hist/hist_2 i
set_directive_bind_op -op mul -impl fabric -latency -1 hist/hist_2 bucket_indx
set_directive_bind_op -op mul -impl fabric -latency -1 hist/hist_2 a_indx
set_directive_bind_op -op add -impl fabric -latency -1 local_scan/local_1 radixID
set_directive_bind_op -op add -impl dsp -latency -1 local_scan/local_2 i
set_directive_bind_op -op mul -impl dsp -latency -1 local_scan/local_2 bucket_indx
set_directive_bind_op -op add -impl dsp -latency -1 sum_scan/sum_1 radixID
set_directive_bind_op -op mul -impl fabric -latency -1 sum_scan/sum_1 bucket_indx
set_directive_bind_op -op add -impl dsp -latency -1 last_step_scan/last_1 radixID
set_directive_bind_op -op add -impl fabric -latency -1 last_step_scan/last_2 i
set_directive_bind_op -op mul -impl fabric -latency -1 last_step_scan/last_2 bucket_indx
set_directive_bind_op -op add -impl fabric -latency -1 update/update_1 blockID
set_directive_bind_op -op mul -impl fabric -latency -1 update/update_2 bucket_indx
set_directive_bind_op -op add -impl fabric -latency -1 update/update_2 i
set_directive_bind_op -op mul -impl fabric -latency -1 update/update_2 a_indx
