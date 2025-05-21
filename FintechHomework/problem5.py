import math

def extended(a:int, b:int) -> tuple[int, int, int]:
    old_r,r=a,b
    old_s,s=1,0
    old_t,t=0,1
    
    while r!=0:
        q=old_r//r
        old_r,r=r,old_r-q*r
        old_s,s=s,old_s-q*s
        old_t,t=t,old_t-q*t
    return old_r, old_s, old_t

def mod_inv(a: int, n: int) -> int:
    d, s, t = extended(a, n)
    if d != 1:
        raise ValueError(f"No modular inverse: gcd({a}, {n}) = {d}")
    return s % n

def crt(remainders:list[int], moduli:list[int])->int:
    N=1
    for ni in moduli:
        N*=ni
    alist=[]
    for ni in moduli:
        try:
            alist.append(mod_inv(N//ni,ni))
        except ValueError:
            return None #서로소 아님
    x=0
    ind=0
    for ri in remainders:
        x+=alist[ind]*ri*(N//moduli[ind])
        ind+=1
    return (x%N)

def bsgs(g: int, h: int, p: int) -> int:
    n = math.ceil(math.sqrt(p))

    baby = []
    for i in range(n + 1):
        baby.append(pow(g, i, p))

    giant = []
    b = mod_inv(pow(g, n, p), p)
    for j in range(n + 1):
        gs = (h * pow(b, j, p)) % p
        if gs in baby:
            k = baby.index(gs)
            x = k + j * n
            return x 
        
def factorint_list(n):
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            factors.append((d, e))
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append((n, 1))
    return factors

def pohlig_hellman(g, h, p):
    n = p - 1
    facs = factorint_list(n)

    rems = []
    mods = []

    for (q, e) in facs:
        qe = q ** e

        g0 = pow(g, n // qe, p)  
        h0 = pow(h, n // qe, p)  

        x_qe = bsgs(g0, h0, p) 
        if x_qe is None:
            print(f"[ERROR] bsgs failed for q = {q}, e = {e}, g0 = {g0}, h0 = {h0}")
            return None
        rems.append(x_qe)
        mods.append(qe)

    return crt(rems, mods)

if __name__ == "__main__":
    p, g, h = 41291799, 17, 192988
    x = pohlig_hellman(g, h, p)
    print(x)
    