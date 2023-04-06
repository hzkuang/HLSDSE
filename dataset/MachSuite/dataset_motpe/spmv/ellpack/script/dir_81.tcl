set_directive_pipeline -off ellpack/ellpack_1
set_directive_pipeline -style stp ellpack/ellpack_2
set_directive_array_reshape -factor 2 -type cyclic ellpack cols
set_directive_bind_op -op add -impl dsp -latency -1 ellpack/ellpack_1 i
set_directive_bind_op -op add -impl dsp -latency -1 ellpack/ellpack_2 j
set_directive_bind_op -op dmul -impl fulldsp -latency -1 ellpack/ellpack_2 Si
set_directive_bind_op -op dadd -impl fulldsp -latency -1 ellpack/ellpack_2 sum
