from sage.all import *


def load_matrix(fname):
    with open(fname, 'r') as f:
        data = f.read().strip()
    rows = [list(map(int, list(row))) for row in data.splitlines()]
    return Matrix(GF(2), rows)


G = load_matrix('generator.txt')
A = load_matrix('flag.enc')


# The discrete log on matrices can be solved by looking at eigenvalues
# in the extension field where the characteristic polynomial splits.
poly = G.charpoly()
factors = poly.factor()


# We use the primary decomposition or simply look at the largest irreducible factor
f, e = factors[-1]
K = GF(2**f.degree(), 'a', modulus=f)
G_k = G.change_ring(K)
A_k = A.change_ring(K)


# Get eigenvalues
eig_G = G_k.eigenvalues()[0]
eig_A = A_k.eigenvalues()[0]


# Solve discrete log: eig_G^x = eig_A
x = discrete_log(eig_A, eig_G)


print(long_to_bytes(int(x)).decode())


