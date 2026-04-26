from sage.all import *
import hashlib


def load_matrix(fname):
    with open(fname, 'r') as f:
        data = f.read().strip()
    rows = [list(map(int, list(row))) for row in data.splitlines()]
    return Matrix(GF(2), rows)


G = load_matrix('generator.txt')
A = load_matrix('alice.pub')
B = load_matrix('bob.pub')


with open('flag.enc', 'r') as f:
    iv_hex = f.readline().strip().split(': ')[1]
    ct_hex = f.readline().strip().split(': ')[1]


# Solve Discrete Log for Alice's secret 'a'
# Characteristic polynomial decomposition
poly = G.charpoly()
factors = poly.factor()


# Use the largest irreducible factor to solve DL in extension field
f, e = factors[-1]
K = GF(2**f.degree(), 'a', modulus=f)
G_k = G.change_ring(K)
A_k = A.change_ring(K)


eig_G = G_k.eigenvalues()[0]
eig_A = A_k.eigenvalues()[0]
a = discrete_log(eig_A, eig_G)


# Compute shared secret: S = B^a
S = B**a


# Derive key and decrypt
shared_str = "".join("".join(map(str, row)) for row in S)
key = hashlib.sha1(shared_str.encode()).digest()[:16]


from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_hex))
flag = unpad(cipher.decrypt(bytes.fromhex(ct_hex)), 16)
print(flag.decode())
