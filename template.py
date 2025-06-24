import sys, time, random, heapq, math, itertools
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


