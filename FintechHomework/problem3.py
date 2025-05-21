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

print("1. ", bsgs(11,21,71))
print("2. ", bsgs(156,116,593))
print("3. ", bsgs(650,2213,3571))