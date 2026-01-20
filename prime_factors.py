def is_prime(x):
    for i in range(2, int(sqrt(x))):
        if x % i == 0:
            return False
    return True

def get_prime_factors(x):
    pf = []
    for i in range(2,x):
        if x % i == 0 and is_prime(x):
            pf.append(x)
    return pf

def get_pf_till(n):
    pf = []
    pfs = {}
    for a in range(2,n):
        pf_a = get_prime_factors(a)
        pf.append(pf_a)
    for l in pf:
        for a in l:
            if a in pfs:
                pfs[a] += 1
            else:
                pfs[a] = 1
    return pfs

print(get_pf_till(100))