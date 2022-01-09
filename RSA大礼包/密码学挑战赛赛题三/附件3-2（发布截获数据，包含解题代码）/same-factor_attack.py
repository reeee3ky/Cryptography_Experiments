import gmpy2
import re
import libnum

Data = []
for i in [1, 18]:
    with open('./Frame' + str(i)) as f:
        data = re.findall('(.{256})(.{256})(.{256})', f.read().strip())
        Data += data

N = [int(n, 16) for n,e,c in Data]
E = [int(e, 16) for n,e,c in Data]
C = [int(c, 16) for n,e,c in Data]

n1, n2 = gmpy2.mpz(N[0]), gmpy2.mpz(N[1])
e1, e2 = gmpy2.mpz(E[0]), gmpy2.mpz(E[1])
c1, c2 = gmpy2.mpz(C[0]), gmpy2.mpz(C[1])
p = gmpy2.gcd(n1, n2)
q1 = n1 // p
q2 = n2 // p
phi_n1 = (p-1) * (q1-1)
phi_n2 = (p-1) * (q2-1)
d1 = gmpy2.invert(e1, phi_n1)
d2 = gmpy2.invert(e2, phi_n2)
m1 = int(pow(c1, d1, n1))
m2 = int(pow(c2, d2, n2))

print('[+] Frame1')
print('p = %d\nq = %d\nn = %d\nphi = %d\ne = %d\nd = %d\nc = %d\nm = %d' %(int(p), int(q1), int(n1), int(phi_n1), int(e1), int(d1), int(c1), int(m1)))
print(int(hex(m1)[2:][16:24], 16), ',', libnum.n2s(m1)[-8:])
print()
print('[+] Frame18')
print('p = %d\nq = %d\nn = %d\nphi = %d\ne = %d\nd = %d\nc = %d\nm = %d' %(int(p), int(q2), int(n2), int(phi_n2), int(e2), int(d2), int(c2), int(m2)))
print(int(hex(m2)[2:][16:24], 16), ',', libnum.n2s(m2)[-8:])