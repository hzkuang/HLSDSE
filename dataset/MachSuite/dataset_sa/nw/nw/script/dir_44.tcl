set_directive_unroll -factor 2 needwun/init_row
set_directive_pipeline -style stp needwun/init_row
set_directive_pipeline -off needwun/init_col
set_directive_unroll -factor 2 needwun/trace
set_directive_pipeline -style stp needwun/trace
set_directive_unroll -factor 2 needwun/pad_a
set_directive_pipeline -off needwun/pad_a
set_directive_pipeline -off needwun/pad_b
set_directive_pipeline -off needwun/fill_in
set_directive_array_reshape -factor 2 -type block needwun SEQB
set_directive_array_partition -factor 2 -type block needwun allignedA
set_directive_array_partition -factor 2 -type cyclic needwun allignedB
set_directive_array_reshape -factor 2 -type block needwun M
set_directive_array_partition -factor 2 -type block needwun ptr
set_directive_bind_op -op mul -impl fabric -latency -1 needwun/fill_in row_up
set_directive_bind_op -op mul -impl dsp -latency -1 needwun/fill_in row
set_directive_bind_op -op add -impl fabric -latency -1 needwun/fill_in up_left
set_directive_bind_op -op add -impl dsp -latency -1 needwun/fill_in up
set_directive_bind_op -op add -impl dsp -latency -1 needwun/fill_in left
set_directive_bind_op -op mul -impl fabric -latency -1 needwun/trace r
set_directive_bind_op -op add -impl dsp -latency -1 needwun/init_row a_idx
set_directive_bind_op -op add -impl dsp -latency -1 needwun/fill_in a_idx
set_directive_bind_op -op sub -impl dsp -latency -1 needwun/trace a_idx
set_directive_bind_op -op add -impl fabric -latency -1 needwun/init_col b_idx
set_directive_bind_op -op add -impl fabric -latency -1 needwun/fill_out b_idx
set_directive_bind_op -op sub -impl fabric -latency -1 needwun/trace b_idx
set_directive_bind_op -op add -impl dsp -latency -1 needwun/trace a_str_idx
set_directive_bind_op -op add -impl dsp -latency -1 needwun/pad_a a_str_idx
set_directive_bind_op -op add -impl dsp -latency -1 needwun/trace b_str_idx
set_directive_bind_op -op add -impl fabric -latency -1 needwun/pad_b b_str_idx
