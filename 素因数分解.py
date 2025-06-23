def prime_factorization(n):   #O(n**0.5)
    import math 
    rtn = []
    temp = n
    for i in range(2, math.isqrt(n)+1):
        if temp % i == 0:
            while temp % i == 0:
                temp = temp // i
                rtn.append(i)
    if temp != 1:
        rtn.append(temp)
    if rtn == []:
        rtn.append(n)
    return rtn


#N=1000
#prime_factorization(N)-> [2,2,2,5,5,5]
#N=77
#prime_factorization(N)-> [7,11]





#https://qiita.com/Kept1994/items/20333987a6d73f435f6d
# 素因数分解

def primeFactrization(n: int):
    # validation check
    if not isinstance(n, int):
        raise("[ERROR] parameter must be integer")
    if n < 0:
        raise("[ERROR] parameter must be not less than 0 (n >= 0)")
    dividableMinimunPrime = [i for i in range(0, n + 1)]      # 数iを割りきる最小の素数
    for i in range(2, int(n ** 0.5 + 1)):
        if dividableMinimunPrime[i] == i:
            for j in range(i ** 2, n + 1, i):
                if dividableMinimunPrime[j] == j:             # 条件を削除して上書きを許可すると得られる素因数が降順になる。
                    dividableMinimunPrime[j] = i
    # ダブリングと同じ要領で進めていく
    primeFactors = []
    rest = n
    while dividableMinimunPrime[rest] != rest:
        primeFactors.append(dividableMinimunPrime[rest])
        rest //= dividableMinimunPrime[rest]
    primeFactors.append(rest)
    return primeFactors

N = 200000
print(primeFactrization(N))
#-> [2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5]



# nまでの各整数について約数の個数を一斉取得
def getNumsOfDivisorsOfEachNumbers(n: int):
    # validation check
    if not isinstance(n, int):
        raise("[ERROR] parameter must be integer")
    if n < 0:
        raise("[ERROR] parameter must be not less than 0 (n >= 0)")
    nums = [0] * (n + 1) # 0-indexed
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            nums[j] += 1
    nums.pop(0)
    return nums


# 約数の個数を一斉取得
#N = 10
#print(getNumsOfDivisorsOfEachNumbers(N))
#-> [1, 2, 2, 3, 2, 4, 2, 4, 3, 4]
