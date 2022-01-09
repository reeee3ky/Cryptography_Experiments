import gmpy2
import re
import libnum

Data = []
for i in [10, 14]:
    with open('./Frame' + str(i)) as f:
        data = re.findall('(.{256})(.{256})(.{256})', f.read().strip())
        Data += data

N = [int(n, 16) for n,e,c in Data]
E = [int(e, 16) for n,e,c in Data]
C = [int(c, 16) for n,e,c in Data]

n1, n2 = gmpy2.mpz(N[0]), gmpy2.mpz(N[1])
e1, e2 = gmpy2.mpz(E[0]), gmpy2.mpz(E[1])
c1, c2 = gmpy2.mpz(C[0]), gmpy2.mpz(C[1])

def fermat(n):
    a = gmpy2.iroot(n, 2)[0] + 1
    b = a * a - n
    p, q = gmpy2.mpz(0), gmpy2.mpz(0)
    # print(a, b)
    while 1:
        if gmpy2.iroot(b, 2)[1] == True:
            b = gmpy2.iroot(b, 2)[0]
            p = a + b
            q = a - b
            break
        a += 1
        b = a * a - n
    return p, q

p1, q1 = fermat(n1)
p2, q2 = fermat(n2)
phi_n1 = (p1-1) * (q1-1)
phi_n2 = (p2-1) * (q2-1)
d1 = gmpy2.invert(e1, phi_n1)
d2 = gmpy2.invert(e2, phi_n2)
m1 = int(pow(c1, d1, n1))
m2 = int(pow(c2, d2, n2))

print('[+] Frame10')
print('p = %d\nq = %d\nn = %d\nphi = %d\ne = %d\nd = %d\nc = %d\nm = %d' %(int(p1), int(q1), int(n1), int(phi_n1), int(e1), int(d1), int(c1), int(m1)))
print(int(hex(m1)[2:][16:24], 16), ',', libnum.n2s(m1)[-8:])
print()
print('[+] Frame14')
print('p = %d\nq = %d\nn = %d\nphi = %d\ne = %d\nd = %d\nc = %d\nm = %d' %(int(p2), int(q2), int(n2), int(phi_n2), int(e2), int(d2), int(c2), int(m2)))
print(int(hex(m2)[2:][16:24], 16), ',', libnum.n2s(m2)[-8:])