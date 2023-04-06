set_directive_pipeline -style stp ellpack/ellpack_1
set_directive_array_partition -factor 2 -type block ellpack nzval
set_directive_array_reshape -factor 2 -type block ellpack nzval
set_directive_array_reshape -factor 2 -type block ellpack cols
set_directive_array_reshape -factor 2 -type block ellpack out
set_directive_bind_op -op add -impl fabric -latency -1 ellpack/ellpack_1 i
set_directive_bind_op -op add -impl dsp -latency -1 ellpack/ellpack_2 j
set_directive_bind_op -op dmul -impl fulldsp -latency -1 ellpack/ellpack_2 Si
set_directive_bind_op -op dadd -impl fabric -latency -1 ellpack/ellpack_2 sum
