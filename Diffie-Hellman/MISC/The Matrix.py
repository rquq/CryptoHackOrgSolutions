from sage.all import *


def binary_to_bytes(bits):
    bin_str = ''.join(str(b) for b in bits)
    return bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))


# Load data
P = 2
N = 50
E = 31337


with open('flag_403b981c77d39217c20390c1729b15f0.enc', 'r') as f:
    data = f.read().strip().splitlines()
    rows = [list(map(int, list(line))) for line in data]


ciphertext = Matrix(GF(P), rows)


# Find E-th root of the matrix
# Since the matrix order is large, we can compute the root via Jordan form or discrete log
# In this specific case, we can use the multiplicative order of the matrix
order = ciphertext.multiplicative_order()
d = pow(E, -1, order)
mat = ciphertext**d


# Extract FLAG from matrix
res_rows = mat.rows()
msg_bits = []
for i in range(N * N):
    msg_bits.append(int(res_rows[i % N][i // N]))


flag = binary_to_bytes(msg_bits)
print(flag.decode().split('}')[0] + '}')
