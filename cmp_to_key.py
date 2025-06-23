#使用例

from functools import cmp_to_key

def cmp(a,b):
    x, y, i = a
    xx, yy, ii = b
    s = x * yy - xx * y
    return s

N = int(input())
X = []
for i in range(N):
    a,b = mi()
    X.append((-a, a+b, i))

X.sort(key = cmp_to_key(cmp))
print(*[x[2] + 1 for x in X])
