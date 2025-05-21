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

problems = [
    (1, 527, 1258),
    (2, 228, 1056),
    (3, 163961, 167181),
    (4, 3892394, 239847)
]

for idx, a, b in problems:
    d, s, t = extended(a, b)
    print(f"{idx}. ({a}, {b}) ⇒ gcd = {d}, s = {s}, t = {t}  →  {a}*{s} + {b}*{t} = {d}")
    
print("======= 총 정리 ======")
print(extended(527,1258))
print(extended(228,1056))
print(extended(163961, 167181))
print(extended(3892394, 239847))