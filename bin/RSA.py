import math
from factordb.factordb import FactorDB
from sympy.ntheory import factorint, isprime

def keypairGen(p, q, e):
    if not isprime(p) or not isprime(q):
        raise ValueError("P or Q are not prime.")
    if p == q:
        phi = (p - 1) * q
    else:
        phi = (p - 1) * (q - 1)
    if math.gcd(e, phi) != 1:
        raise ValueError("e and phi are not coprime.")
    d = pow(e, -1, phi)
    n = p * q
    Kpub = (e, n)
    Kpriv = (d, n)
    return Kpub, Kpriv
    
def encRSA(text, kpub):
    m = int.from_bytes(text.encode(), "big")
    e, n = kpub
    ct = pow(m, e, n)
    return ct

def decRSA(ct, kpub, kpriv):
    e, n = kpub
    d, _ = kpriv
    m = pow(ct, d, n)
    print(m)
    return int.to_bytes(m, (m.bit_length() + 7) // 8  , "big")


def attack(kpub, ct):
    e, n = kpub
    f = FactorDB(n)
    f.connect()
    status = f.get_status()
    if status == "FF" or status == "P":
        factors = f.get_factor_from_api()
        factors = [tuple([int(fa[0]), fa[1]]) for fa in factors]
    else:
        factors = factorint(n)
        factors = list(factors.items())
    
    phi = 1
    for factor in factors:
        phi *= (factor[0] - 1)
        phi *= (pow(factor[0], factor[1] - 1))
    d = pow(e, -1, phi)
    kpriv = (d, n)
    return decRSA(ct, kpub, kpriv), factors

# if __name__ == "__main__":
#     message = "Hello World"
#     e = 17
#     p = 833849682377741
#     q = 11
#     kpub, kpriv = keypairGen(p, q, e)
#     ct = encRSA(message, kpub)
#     print(decRSA(ct, kpub, kpriv))
#     print(attack(kpub, ct))