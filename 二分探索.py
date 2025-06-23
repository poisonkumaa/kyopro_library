#めぐる式二分探索？

def check(mid):
    #内容がないよう
    return 0

ok=0
ng=10**9

while ng - ok > 1:
    mid = (ng + ok) // 2
    if check(mid):
        ok = mid
    else:
        ng = mid

print(ok)
