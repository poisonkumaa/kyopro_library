# エラトステネスの篩
#案1  
#https://qiita.com/Mopepe51/items/cce17bce6acbb4c25795
#O(nloglogn)

def eratosthenes(n):
    is_prime = ([False, True] * (n//2+1))[0: n+1]
    is_prime[1] = False
    is_prime[2] = True
    for i in range(3, n+1, 2):
        if not(is_prime[i]):
            continue
        if i*i > n:
            break
        for k in range(i*i, n+1, i):
            is_prime[k] = False
    return [i for i in range(n+1) if is_prime[i]] 

#print(eratosthenes(97))
#-> [2,3, ... 97]

#案2
# 素数列挙 (区間指定可)
def getPrimes(last: int, first: int = 1):
    # validation check
    if not isinstance(last, int) or \
        not isinstance(first, int):
        raise("[ERROR] parameter must be integer")
    if last < 0 or first < 0:
        raise("[ERROR] parameter must be not less than 0 (first >= 0 & last >= 0)")
    
    if last < first:
        last, first = first, last
    isPrime = [True] * (last + 1)    # 素数かどうか
    # 0と1をFalseに
    isPrime[0] = isPrime[1] = False
    for i in range(2, int(last ** 0.5 + 1)):
        if isPrime[i]:
            # 篩にかける。iの倍数をすべてFalseにしていく。このとき i^2まではすでにふるい落とされているので見る必要がない
            for j in range(i ** 2, last + 1      , i):
                isPrime[j] = False
    return [i for i in range(first, last + 1) if isPrime[i]] 

#print(getPrimes(1000))
#計算量O(nlog(n))
#10^9以下の最大の素数は999999937
