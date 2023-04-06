set_directive_inline aes_expandEncKey
set_directive_inline aes_addRoundKey_cpy
set_directive_inline -off aes_subBytes
set_directive_inline aes_shiftRows
set_directive_inline aes_mixColumns
set_directive_inline -off aes_addRoundKey
set_directive_unroll -factor 2 aes256_encrypt_ecb/ecb1
set_directive_pipeline -off aes256_encrypt_ecb/ecb1
set_directive_pipeline -style stp aes256_encrypt_ecb/ecb2
set_directive_pipeline -off aes256_encrypt_ecb/ecb3
set_directive_array_reshape -factor 2 -type cyclic aes256_encrypt_ecb k
set_directive_array_partition -factor 2 -type cyclic aes256_encrypt_ecb buf
set_directive_array_reshape -factor 2 -type block aes256_encrypt_ecb buf
set_directive_bind_op -op add -impl fabric -latency -1 aes256_encrypt_ecb/ecb1 i
set_directive_bind_op -op sub -impl fabric -latency -1 aes256_encrypt_ecb/ecb2 i
set_directive_bind_op -op add -impl fabric -latency -1 aes256_encrypt_ecb/ecb3 i
