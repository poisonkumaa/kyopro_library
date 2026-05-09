
import sys, time, random, heapq, math, itertools, copy
from collections import deque, Counter, defaultdict
from sortedcontainers import SortedSet, SortedList
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
dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# O(N^3 * logK)


def get_mincost(A: list, K: int):
    """
    A[i][j]: 頂点iからjへ有向グラフが張っており、その移動コスト(なければinf)
    以上の隣接行列に基づいたグラフについて、rtn[i][j]:
    頂点 iから出発し、辺に沿って移動することを K 回繰り返して頂点 j へ向かう方法のうち、
    通った辺のコストの総和としてありうる最小値。
    と定義。
    """
    
    N = len(A)
    dp = [[[0]*N for _ in range(N)] for _ in range(65)]
    for i in range(N):
        for j in range(N):
            dp[0][i][j] = A[i][j]

    for bit in range(64):
        for i in range(N):
            for j in range(N):
                temp = []
                for k in range(N):
                    temp.append(dp[bit][i][k] + dp[bit][k][j])
                dp[bit+1][i][j] = min(temp)

    # 単位元
    rtn = [[inf] * N for _ in range(N)]
    for i in range(N):
        rtn[i][i] = 0

    bit = 0
    while K:
        if K & 1:
            new = [[[0] for _ in range(N)] for _ in range(N)]
            for i in range(N):
                for j in range(N):
                    temp = []
                    for k in range(N):
                        temp.append(dp[bit][i][k] + rtn[k][j])
                    new[i][j] = min(temp)
            rtn = new
        K //= 2
        bit += 1
        
    return rtn


if __name__ == "__main__":
    """
    g = [[3, 1, 4, 1,],
         [5, 9, 2, 6,],
         [5, 3, 5, 8,],
         [9, 7, 9, 3,]]
    """
    N, K = mi()
    g = [li() for _ in range(N)]
    cost = get_mincost(g, K)
    print(cost)    
