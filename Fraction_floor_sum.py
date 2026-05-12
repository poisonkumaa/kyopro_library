"""
    ABC230-E 解法コード "https://atcoder.jp/contests/abc230/tasks/abc230_e"
    sigma(_1 ^N)[i] (N//i) をO(sqrt(N))計算する
    
    [N/i] = k
<=>  k<= N/i < k+1 を満たすiをkで表すと、
    N/(k+1) < i <= N/k   -> iはN//k - N//(k+1) 個存在
    1<=k<sqrt(N) ではi == 1
    N//k - N//(k+1) >= 1 となるとき、 k <= sqrt(N)
    また、そうではない時、つまり k>=sqrt(N)+1 <=> [N/i]>=sqrt(N)+1 であるとき、それらは高々一個であるので
    足し合わせればよい。([N/i] >= sqrt(N) + 1 より N//(sqrt(N) + 1) >= i  )

"""



import sys, math
input = lambda: sys.stdin.readline().rstrip()
ii = lambda: int(input())
mi = lambda: map(int, input().split())
li = lambda: list(mi())

N = ii()
Ns = math.isqrt(N)
ans = 0
for k in range(1,Ns+1):
    ans += k * (N//k - N//(k+1))
for i in range(1, N//(Ns+1)+1):
    ans += N//i
print(ans)

    
