from sympy import factorint

n = 510143758735509025530880200653196460532653147
factors = list(factorint(n).keys())
flag = min(factors)

print(flag)
