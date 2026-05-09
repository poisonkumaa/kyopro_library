#めぐる式二分探索

def check(mid):
    #内容
    return 0

ok=0
ng=2**61-1

while ng - ok > 1:
    mid = (ng + ok) // 2
    if check(mid):
        ok = mid
    else:
        ng = mid

print(ok)
