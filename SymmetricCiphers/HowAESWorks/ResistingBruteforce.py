import math

bits_standard = 128
bits_biclique = 126.1

complexity_standard = 2 ** bits_standard
complexity_biclique = 2 ** bits_biclique

ratio = complexity_standard / complexity_biclique

print(f"Standard Complexity: 2^{bits_standard}")
print(f"Biclique Complexity: 2^{bits_biclique}")
print(f"Improvement Factor: {ratio:.2f}x faster")