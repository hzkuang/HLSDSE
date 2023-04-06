set_directive_pipeline -style stp bfs/loop_neighbors
set_directive_array_reshape -factor 2 -type block bfs nodes
set_directive_array_partition -factor 2 -type block bfs edges
set_directive_array_partition -factor 2 -type cyclic bfs level
set_directive_array_reshape -factor 2 -type cyclic bfs level
set_directive_array_partition -factor 2 -type cyclic bfs level_counts
set_directive_array_reshape -factor 2 -type block bfs level_counts
set_directive_bind_op -op add -impl fabric -latency -1 bfs/loop_horizons horizon
set_directive_bind_op -op add -impl fabric -latency -1 bfs/loop_nodes n
set_directive_bind_op -op add -impl fabric -latency -1 bfs/loop_neighbors e
set_directive_bind_op -op add -impl fabric -latency -1 bfs/loop_neighbors cnt
