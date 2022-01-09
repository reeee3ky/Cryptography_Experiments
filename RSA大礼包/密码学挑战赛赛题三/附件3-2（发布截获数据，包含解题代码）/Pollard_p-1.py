import gmpy2
import re
import libnum

Data = []
for i in [2, 6, 19]:
    with open('./Frame' + str(i)) as f:
        data = re.findall('(.{256})(.{256})(.{256})', f.read().strip())
        Data += data

N = [int(n, 16) for n,e,c in Data]
E = [int(e, 16) for n,e,c in Data]
C = [int(c, 16) for n,e,c in Data]

n1, n2, n3 = gmpy2.mpz(N[0]), gmpy2.mpz(N[1]), gmpy2.mpz(N[2])
e1, e2, e3 = gmpy2.mpz(E[0]), gmpy2.mpz(E[1]), gmpy2.mpz(E[2])
c1, c2, c3 = gmpy2.mpz(C[0]), gmpy2.mpz(C[1]), gmpy2.mpz(C[2])

def Pollard(n):
    a = i = 2
    while 1:
        a = gmpy2.powmod(a, i, n)
        p = gmpy2.gcd(a-1, n)
        if p != 1:
            q = n // p
            return p, q
        i += 1

p1, q1 = Pollard(n1)
p2, q2 = Pollard(n2)
p3, q3 = Pollard(n3)
phi_n1 = (p1-1) * (q1-1)
phi_n2 = (p2-1) * (q2-1)
phi_n3 = (p3-1) * (q3-1)
d1 = gmpy2.invert(e1, phi_n1)
d2 = gmpy2.invert(e2, phi_n2)
d3 = gmpy2.invert(e3, phi_n3)
m1 = int(pow(c1, d1, n1))
m2 = int(pow(c2, d2, n2))
m3 = int(pow(c3, d3, n3))

print('[+] Frame2')
print('p = %d\nq = %d\nn = %d\nphi = %d\ne = %d\nd = %d\nc = %d\nm = %d' %(int(p1), int(q1), int(n1), int(phi_n1), int(e1), int(d1), int(c1), int(m1)))
print(int(hex(m1)[2:][16:24], 16), ',', libnum.n2s(m1)[-8:])
print()
print('[+] Frame6')
print('p = %d\nq = %d\nn = %d\nphi = %d\ne = %d\nd = %d\nc = %d\nm = %d' %(int(p2), int(q2), int(n2), int(phi_n2), int(e2), int(d2), int(c2), int(m2)))
print(int(hex(m2)[2:][16:24], 16), ',', libnum.n2s(m2)[-8:])
print()
print('[+] Frame19')
print('p = %d\nq = %d\nn = %d\nphi = %d\ne = %d\nd = %d\nc = %d\nm = %d' %(int(p3), int(q3), int(n3), int(phi_n3), int(e3), int(d3), int(c3), int(m3)))
print(int(hex(m3)[2:][16:24], 16), ',', libnum.n2s(m3)[-8:])