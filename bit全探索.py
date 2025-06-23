#No1
#Atcoder_separated lunchより

N = int(input())
K=list(map(int,input().split()))
ans=10**9

for bit in range(1 << N):  # 1 << N は 2^N と同じ, 2択×N個
    a,b = 0,0
    for i in range(N):  # どこにbitが立ってるかを確認していく
        if bit & (1 << i):  # 下からi番目にbitが立っているとき
            a += K[i]
        else:
            b += K[i]
    ans = min(ans,max(a,b))

print(ans)

#----------------------------------------------------------------------------------
"""
#No2
S = input()
N = len(S)
ans = 0
N=100    #Length
for b in range(2 ** (N - 1)):
    bit = bin(b)[2:].zfill(N - 1)
    s = S[0]
    for i in range(N - 1):  # どこにbitが立ってるかを確認していく
        if bit[i] == "1":  # 下からi番目にbitが立っているとき
            ans += int(s)
            s = ""
        s += S[i + 1]
    ans += int(s)
print(ans)


#--------------------------------------------------------------------------


#No3
from itertools import product

S = input()
N = len(S)
ans = 0

# Sに+を挟む方法は、Sに文字と文字の間(N-1個ある)に
# それぞれ挟むか挟まないかを決めれば決まるから2^(N-1)通りある。

# それを長さN-1のbitに対応させることで全探索することで答えを求める。
# 例: S = 12345 bit = 110 なら bit = 0110 とみなして 12+3+45 を答えに足していく。

for bit in product((0, 1), repeat=N - 1):
    s = S[0]
    for i in range(N - 1):  # どこにbitが立ってるかを確認していく
        if bit[i] == 1:  # 下からi番目にbitが立っているとき
            ans += int(s)
            s = ""
        s += S[i + 1]
    ans += int(s)
print(ans)

"""
