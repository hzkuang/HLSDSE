set_directive_loop_flatten -off stencil3d/height_bound_col
set_directive_pipeline -off stencil3d/height_bound_col
set_directive_unroll -factor 2 stencil3d/height_bound_row
set_directive_pipeline -style stp stencil3d/height_bound_row
set_directive_loop_flatten -off stencil3d/col_bound_height
set_directive_pipeline -style stp stencil3d/col_bound_height
set_directive_loop_flatten stencil3d/row_bound_height
set_directive_unroll -factor 2 stencil3d/row_bound_col
set_directive_pipeline -style stp stencil3d/row_bound_col
set_directive_loop_flatten stencil3d/loop_height
set_directive_loop_flatten -off stencil3d/loop_col
set_directive_unroll -factor 2 stencil3d/loop_col
set_directive_pipeline -style stp stencil3d/loop_col
set_directive_array_reshape -factor 2 -type cyclic stencil3d orig
set_directive_array_partition -factor 2 -type block stencil3d sol
set_directive_array_reshape -factor 2 -type block stencil3d sol
set_directive_bind_op -op add -impl dsp -latency -1 stencil3d/loop_row sum1
set_directive_bind_op -op mul -impl fabric -latency -1 stencil3d/loop_row mul0
set_directive_bind_op -op mul -impl fabric -latency -1 stencil3d/loop_row mul1
