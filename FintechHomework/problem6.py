import random

def is_prime(n: int, k: int = 10) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

test_values = [
    1105,
    294409,
    294439,
    118901509,
    118901521,
    118901527,
    118915387,
]

for n in test_values:
    print(f"{n}: {is_prime(n)}")