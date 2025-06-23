#約数列挙、O(N**0.5)
#https://qiita.com/LorseKudos/items/9eb560494862c8b4eb56
def make_divisors(n):
    lower_divisors , upper_divisors = [], []
    i = 1
    while i*i <= n:
        if n % i == 0:
            lower_divisors.append(i)
            if i != n // i:
                upper_divisors.append(n//i)
        i += 1
    return lower_divisors + upper_divisors[::-1]

#事前計算パターン、前計O(MlogM)
M = 10**6 + 1
divisors = [[] for _ in range(M)]
for i in range(1, M):
    for j in range(i, M, i):
        divisors[j].append(i)