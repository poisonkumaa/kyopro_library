"""
A = [A_0, A_1, ... A_(N-1)] かつA_0 <= A_1 <= ... <= A_(N-1)が成り立っているとき
「隙間ではなくindexを返すことを意識する!!!!」

・基本は
bisect_left(A, t): A[i] >= t を満たす最小のインデックスを返す（t以上の境界）

bisect_right(A, t): A[i] > t を満たす最小のインデックスを返す（tより大きいの境界）


・Aからt以下で最大のものを見つけたいとき
t より大きい要素が始まる場所の「1つ左」を見ます。
インデックスの取得: idx = bisect_right(A, t) - 1
要素の取得: A[idx]
注意: idx == -1 の場合、配列内に t 以下の要素は存在しません。


・Aからt未満で最大のものを見つけたいとき
t 以上の要素が始まる場所の「1つ左」を見ます。
インデックスの取得: idx = bisect_left(A, t) - 1
要素の取得: A[idx]
注意: idx == -1 の場合、配列内に t 未満の要素は存在しません。


・Aからt以上で最小のものを見つけたいとき
bisect_left の挙動そのものです。
インデックスの取得: idx = bisect_left(A, t)
要素の取得: A[idx]
注意: idx == len(A) の場合、配列内に t 以上の要素は存在しません。


・Aからtより大きいもので最小のものを見つけたいとき
bisect_right の挙動そのものです。
インデックスの取得: idx = bisect_right(A, t)
要素の取得: A[idx]
注意: idx == len(A) の場合、配列内に t より大きい要素は存在しません。
"""

# 以下に例を示す

from bisect import bisect_left, bisect_right

A = [10, 20, 20, 30, 40]
t = 20

# 1. t以下で最大 (答え: 20, idx: 2)
idx1 = bisect_right(A, t) - 1
if idx1 >= 0:
    print(f"{t}以下で最大: {A[idx1]}")

# 2. t未満で最大 (答え: 10, idx: 0)
idx2 = bisect_left(A, t) - 1
if idx2 >= 0:
    print(f"{t}未満で最大: {A[idx2]}")

# 3. t以上で最小 (答え: 20, idx: 1)
idx3 = bisect_left(A, t)
if idx3 < len(A):
    print(f"{t}以上で最小: {A[idx3]}")

# 4. tより大きいもので最小 (答え: 30, idx: 3)
idx4 = bisect_right(A, t)
if idx4 < len(A):
    print(f"{t}より大きい最小: {A[idx4]}")