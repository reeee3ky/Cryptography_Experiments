# coding=utf-8
import re
import gmpy2
import libnum
from functools import *

# 中国剩余定理
def CRT(C, N):
	mul_n = reduce(lambda x, y: x * y, N)
	result = 0
	for a, n in zip(C, N):
		m = mul_n // n
		d, r, s = gmpy2.gcdext(n, m)
		result += a * s * m
	return result % mul_n, mul_n

# 按照格式分割数据
Data = []
N = []
C = []
for i in [3, 8, 12, 16, 20]:
    with open('./Frame' + str(i)) as f:
        data = re.findall('(.{256})(.{256})(.{256})', f.read().strip())
        Data += data

N = [int(n, 16) for n,e,c in Data]
C = [int(c, 16) for n,e,c in Data]
e = 5
c, n = CRT(C, N)
m = int(gmpy2.iroot(gmpy2.mpz(c), e)[0])
print(int(hex(m)[2:][16:24], 16), ',', libnum.n2s(m)[-8:])