#[L,R]の素因数分解をO(max(R-L, root(R)))で計算可能
import math

#以下の素数を列挙
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

#区間篩
def kukanhurui(L,R):
    if L > R:
        return []
    primes = eratosthenes(math.isqrt(R))
    A = [i for i in range(L, R+1)]
    divisors = [[] for _ in range(R-L+1)]
    for p in primes:
        start = (-L) % p 
        for i in range(start, R-L+1, p):
            while A[i] % p == 0:
                divisors[i].append(p)
                A[i] //= p
    for i in range(R-L+1):
        if A[i] != 1:
            divisors[i].append(A[i])

    return divisors

#print(kukanhurui(3,10))
#[[3], [2, 2], [5], [2, 3], [7], [2, 2, 2], [3, 3], [2, 5]]




#素数の個数のみ取得したい場合、O((B-A)loglogB)
#https://algo-method.com/tasks/332/editorial

import math

def is_prime_num(A,B):

    # √B 以下の素数を炙り出すための篩
    sqrtB = int(math.sqrt(B) + 0.1)
    isprime = [True] * (sqrtB + 1)

    # A 以上 B 以下の整数 v が素数かどうか
    # その答えは isprime2[v-A] に格納される
    isprime2 = [True] * (B - A + 1)

    # ふるい
    for p in range(2, sqrtB + 1):
    # すでに合成数であるものはスキップする
        if not isprime[p]:
            continue

        # p 以外の p の倍数から素数ラベルを剥奪
        q = p * 2
        while q * q <= B:
            isprime[q] = False
            q += p

        # A 以上の最小の p の倍数
        start = A + (-A) % p
        if start == p:
            start = p * 2

        # A 以上 B 以下の整数のうち、p の倍数をふるう
        q = start
        while q <= B:
            isprime2[q - A] = False
            q += p

    return sum(isprime2)

#print(is_prime_num(7,13)) -> 3
