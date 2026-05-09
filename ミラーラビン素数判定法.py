#確率的素数判定法
#n：判定する素数
#k：判定の精度

import random

def isprime(n, k):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    d = n-1
    s = 0
    while d % 2 == 0:
        d = d // 2 
        s += 1

    for _ in range(k):
        a = random.randint(1, n-1)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        
        for _ in range(s):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False

    return True
            

print(isprime(100000000000000003, 1000))
# -> True

print(isprime(10**100 + 1, 1000))
# -> False
