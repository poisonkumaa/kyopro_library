#paiza_s072より
#鉄則本p139のpython版

import sys
input = lambda: sys.stdin.readline().rstrip()
ii = lambda: int(input())
mi = lambda: map(int, input().split())
li = lambda: list(mi())
inf = 2 ** 61 -1   

#入力
N, C = mi()
K = ii()
p = [list(map(int,input())) for _ in range(K)]

#bitDPで解く
#dp[i][j] : iパックまでのいくつかを選んだ時、カードの集合がjである状態を考えたとき、選んだ最小パック数
dp = [[inf] * (1 << N) for _ in range(K+1)]
dp[0][0] = 0

for i in range(1, K + 1):
    for j in range(1 << N):
        if dp[i-1][j] == inf: continue
        already = [0] * N 
        for k in range(N):
            if j & (1 << k): 
                already[k] = 1
        v = 0
        for k in range(N):
            if already[k] == 1 or p[i-1][k] == 1:
                v += (1 << k)
        
        #dpの遷移
        dp[i][j] = min(dp[i][j], dp[i-1][j])
        dp[i][v] = min(dp[i][v], dp[i-1][j] + 1)

if dp[K][(1 << N) - 1] == inf:
    print(-1)
    exit()
else:
    print(dp[i][(1 << N) - 1])


