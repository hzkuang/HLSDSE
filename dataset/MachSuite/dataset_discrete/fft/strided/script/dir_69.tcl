set_directive_unroll -factor 2 fft/outer
set_directive_pipeline -off fft/outer
set_directive_unroll -factor 2 fft/inner
set_directive_pipeline -style stp fft/inner
set_directive_array_partition -factor 2 -type block fft real
set_directive_array_reshape -factor 2 -type block fft img
set_directive_array_partition -factor 2 -type block fft img_twid
set_directive_bind_op -op add -impl fabric -latency -1 fft/inner odd
set_directive_bind_op -op add -impl fabric -latency -1 fft/outer log
set_directive_bind_op -op dadd -impl fulldsp -latency -1 fft/inner temp
set_directive_bind_op -op dmul -impl fabric -latency -1 fft/inner temp
