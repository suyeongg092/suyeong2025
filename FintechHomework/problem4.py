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

print("1. ", crt([3, 4], [7, 9]))
print("2. ", crt([137, 87], [423, 191]))
print("3. ", crt([133, 237], [451, 697]))
print("4. ", crt([5, 6, 7], [9, 10, 11]))
print("5. ", crt([37, 22, 18], [43, 49, 71]))