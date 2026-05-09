#ABC367-E
#ダブリング～
#dp[i][j]: 2**i回遷移した後において、jがどこにあるか
#ans_idx[i]: iがK回遷移した後どこにあるか、
#X : 遷移
#A : 初期位置


N, K = map(int,input().split())
X = list(map(int,input().split()))
A = list(map(int,input().split()))
dp = [[0] * N for _ in range(65)]
for i in range(N):
    dp[0][i] = X[i]-1

for i in range(64):
    for j in range(N):
        #ダブリングの遷移式
        dp[i+1][j] = dp[i][dp[i][j]]

ans_idx = [i for i in range(N)]
for i in range(64):
    if K & (1 << i):
        temp = [-1] * N
        for j in range(N):
            temp[j] = ans_idx[dp[i][j]]
        ans_idx = temp
print(*[A[i] for i in ans_idx])

