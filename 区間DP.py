import sys, time, random, heapq, math, itertools
from collections import deque, Counter, defaultdict
#from sortedcontainers import SortedSet, SortedList
from bisect import bisect, bisect_left, bisect_right
import heapq as hq
from functools import cache, cmp_to_key
def debug(*x):print('debug:',*x, file=sys.stderr)
sys.setrecursionlimit(300000)
input = lambda: sys.stdin.readline().rstrip()
ii = lambda: int(input())
mi = lambda: map(int, input().split())
li = lambda: list(mi())
inf = 2 ** 61 - 1
mod = 998244353


# https://onlinejudge.u-aizu.ac.jp/challenges/sources/ICPC/Prelim/1611?year=2016

# 区間DP
# DP[l][r]: 区間[l, r]で除去できる最大数
# 遷移1. w[l]とw[r]がペアになって除去される：区間[l+1, r-1]はすべて除去でき，かつabs(w[l]-w[r])<=1
# 遷移2. 区間[l,i]と区間[i+1,r]に分けて考える


while True:
    N = ii()
    if N == 0: break
    w = li()
    dp = [[0] * N for _ in range(N)]  #dp[i][j] [i,j]区間で落とせる最大の要素数
    for d in range(1, N):
        for l in range(N):
            r = l + d
            if r >= N:
                break
            if d == 1:
                if abs(w[l] - w[r]) <= 1:
                    dp[l][r] = 2
                continue
            # 遷移2

            for mid in range(l, r):
                dp[l][r] = max(dp[l][r], dp[l][mid] + dp[mid+1][r])
            # 遷移1
            if dp[l+1][r-1] == d-1 and abs(w[l] - w[r]) <= 1:
                dp[l][r] = d+1
    print(dp[0][N-1])
