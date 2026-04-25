from math import gcd
from sympy import isprime
s = [588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237]

diffs = []
for i in range(len(s) - 2):
    diffs.append(abs(s[i+1]**2 - s[i]*s[i+2]))

common_gcd = diffs[0]
for d in diffs[1:]:
    common_gcd = gcd(common_gcd, d)

def get_three_digit_prime(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            for factor in [i, n // i]:
                if 100 <= factor <= 999 and isprime(factor):
                    return factor
    return n if (100 <= n <= 999 and isprime(n)) else None
p = get_three_digit_prime(common_gcd)
x = (s[1] * pow(s[0], -1, p)) % p
print(f"crypto{{{p},{x}}}")