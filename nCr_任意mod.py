#前計算O(N ** 2)、取得O(1)
#N >= n >= r に対してnCrを取得可能

def cmb(max_n, mod):
    CMB = CMB = [[0] * (max_n + 1) for _ in range(max_n + 1)]
    for n in range(max_n + 1):
        CMB[n][0] = 1
        for r in range(1, n + 1):
            CMB[n][r] = (CMB[n - 1][r - 1] + CMB[n - 1][r]) % mod
            
    return CMB
