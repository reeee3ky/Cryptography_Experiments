# coding=utf-8
import gmpy2
import libnum
import re

Data = []
for i in [0, 4]:
    with open('./Frame' + str(i)) as f:
        data = re.findall('(.{256})(.{256})(.{256})', f.read().strip())
        Data += data

E = [int(e, 16) for n,e,c in Data]
C = [int(c, 16) for n,e,c in Data]
N = [int(n, 16) for n,e,c in Data]

n = N[0]
c1, c2 = C[0], C[1]
e1, e2 = E[0], E[1]
_, s1, s2 = gmpy2.gcdext(e1, e2) # s1*e1 + s2*e2 = 1

# 若 s1 < 0，则 c1^s1 == (c1^-1)^(-s1)，其中 c1^-1 为 c1 模 n 的逆元
if s1 < 0:
    s1 = -s1
    c1 = gmpy2.invert(c1, n)
if s2 < 0:
    s2 = -s2
    c2 = gmpy2.invert(c2, n)

m = int(pow(c1, s1, n) * pow(c2, s2, n) % n)
print(int(hex(m)[2:][16:24], 16), ',', libnum.n2s(m)[-8:])