# エラトステネスの篩
#https://qiita.com/Mopepe51/items/cce17bce6acbb4c25795
#O(nloglogn)
def eratosthenes(n):
    if n == 1:
        return []
    is_prime = ([False, True] * (n//2+1))[0: n+1]
    is_prime[1] = False
    is_prime[2] = True
    for i in range(3, n+1, 2):
        if not(is_prime[i]):
            continue
        if i*i > n:
            break
        for k in range(i*i, n+1, 2*i):
            is_prime[k] = False
    return [i for i in range(n+1) if is_prime[i]] 

#print(eratosthenes(97))
#-> [2,3, ... 97]

#改良版
#N以下について素因数分解する
#O(nloglogn)
def eratosthenes_n(n):
    primes = eratosthenes(n)  #n以下の素数
    A = [i for i in range(n+1)]
    divisors = [[] for _ in range(n+1)]
    for p in primes:
        for i in range(p, n+1, p):
            while A[i] % p == 0:
                divisors[i].append(p)
                A[i] /= p
    return divisors

#print(eratosthenes_n(10))
#-> [[], [], [2], [3], [2, 2], [5], [2, 3], [7], [2, 2, 2], [3, 3], [2, 5]]


