P.<x> = PolynomialRing(GF(2))
F.<a> = GF(2^128, modulus=x^128 + x^7 + x^2 + x + 1)
PR.<H> = PolynomialRing(F)

def bytes_to_element(b):
    return F.fetch_int(int.from_bytes(b, 'big'))

def element_to_bytes(e):
    return int(e.integer_representation()).to_bytes(16, 'big')

def ghash_poly(A, C):
    blocks = []
    if len(A) > 0:
        blocks += [A[i:i+16].ljust(16, b'\x00') for i in range(0, len(A), 16)]
    if len(C) > 0:
        blocks += [C[i:i+16].ljust(16, b'\x00') for i in range(0, len(C), 16)]
    
    len_block = (len(A)*8).to_bytes(8, 'big') + (len(C)*8).to_bytes(8, 'big')
    blocks.append(len_block)
    
    poly = 0
    for i, block in enumerate(blocks):
        poly += bytes_to_element(block) * H**(len(blocks) - i)
    return poly

def forge_tag(A1, C1, T1, A2, C2, T2, A_target, C_target):
    poly1 = ghash_poly(A1, C1) + bytes_to_element(T1)
    poly2 = ghash_poly(A2, C2) + bytes_to_element(T2)
    
    combined_poly = poly1 + poly2
    roots = combined_poly.roots()
    
    for r, _ in roots:
        H_guess = r
        EK_J0 = ghash_poly(A1, C1)(H_guess) + bytes_to_element(T1)
        T_target_element = ghash_poly(A_target, C_target)(H_guess) + EK_J0
        return element_to_bytes(T_target_element)

A1 = bytes.fromhex("TỰ_ĐIỀN_ASSOCIATED_DATA_1_VÀO_ĐÂY")
C1 = bytes.fromhex("TỰ_ĐIỀN_CIPHERTEXT_1_VÀO_ĐÂY")
T1 = bytes.fromhex("TỰ_ĐIỀN_TAG_1_VÀO_ĐÂY")

A2 = bytes.fromhex("TỰ_ĐIỀN_ASSOCIATED_DATA_2_VÀO_ĐÂY")
C2 = bytes.fromhex("TỰ_ĐIỀN_CIPHERTEXT_2_VÀO_ĐÂY")
T2 = bytes.fromhex("TỰ_ĐIỀN_TAG_2_VÀO_ĐÂY")

A_target = bytes.fromhex("TỰ_ĐIỀN_ASSOCIATED_DATA_MỤC_TIÊU_VÀO_ĐÂY")
C_target = bytes.fromhex("TỰ_ĐIỀN_CIPHERTEXT_MỤC_TIÊU_VÀO_ĐÂY")

forged_tag = forge_tag(A1, C1, T1, A2, C2, T2, A_target, C_target)
print(forged_tag.hex())