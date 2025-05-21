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

print("(37,45)의 역원:", mod_inv(37, 45))
#역원이 맞는지 확인하기
print("(37 × 28) mod 45 ==", (37*28)%45) 