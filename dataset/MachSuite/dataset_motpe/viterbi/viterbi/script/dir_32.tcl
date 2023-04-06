set_directive_pipeline -off viterbi/L_init
set_directive_pipeline -off viterbi/L_end
set_directive_pipeline -off viterbi/L_backtrack
set_directive_pipeline -off viterbi/L_state
set_directive_loop_flatten viterbi/L_timestep
set_directive_pipeline -off viterbi/L_curr_state
set_directive_pipeline -off viterbi/L_prev_state
set_directive_bind_storage -type ram_s2p -impl bram -latency -1 viterbi llike
set_directive_array_partition -factor 2 -type block viterbi obs
set_directive_array_reshape -factor 2 -type block viterbi obs
set_directive_array_reshape -factor 2 -type block viterbi init
set_directive_array_partition -factor 2 -type cyclic viterbi transition
set_directive_array_reshape -factor 2 -type block viterbi transition
set_directive_array_partition -factor 2 -type cyclic viterbi emission
set_directive_array_reshape -factor 2 -type block viterbi emission
set_directive_array_reshape -factor 2 -type cyclic viterbi path
set_directive_bind_op -op add -impl fabric -latency -1 viterbi/L_timestep t
set_directive_bind_op -op sub -impl dsp -latency -1 viterbi/L_backtrack t
set_directive_bind_op -op add -impl fabric -latency -1 viterbi/L_prev_state prev
set_directive_bind_op -op add -impl fabric -latency -1 viterbi/L_curr_state curr
set_directive_bind_op -op add -impl fabric -latency -1 viterbi/L_init s
set_directive_bind_op -op add -impl fabric -latency -1 viterbi/L_end s
set_directive_bind_op -op add -impl fabric -latency -1 viterbi/L_state s
set_directive_bind_op -op dadd -impl fabric -latency -1 viterbi/L_curr_state min_p
set_directive_bind_op -op dadd -impl fulldsp -latency -1 viterbi/L_backtrack min_p
set_directive_bind_op -op dadd -impl fabric -latency -1 viterbi/L_prev_state p
set_directive_bind_op -op dadd -impl fabric -latency -1 viterbi/L_state p
