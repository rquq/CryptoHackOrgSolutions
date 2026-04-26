p = 28151
phi = p - 1


def get_prime_factors(n):
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors


factors = get_prime_factors(phi)


def is_primitive(g, p, factors):
    for q in factors:
        if pow(g, (p - 1) // q, p) == 1:
            return False
    return True


g = 2
while True:
    if is_primitive(g, p, factors):
        print(g)
        break
    g += 1
