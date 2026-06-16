def extended_euclid(a: int, b: int) -> tuple[int, int]:
    """
    aX + bY = 1 を満たす特殊解 (X, Y) のうち、0 <= X < |b| となるものを返す。
    gcd(a, b) != 1 の場合は ValueError を送出する。
    """
    def _rec(aa, bb):
        if bb == 0:
            return 1, 0, aa
        x, y, g = _rec(bb, aa % bb)
        return y, x - (aa // bb) * y, g

    x0, _, g = _rec(abs(a), abs(b))

    if g != 1:
        raise ValueError(f"gcd({a}, {b}) != 1 です。解が存在しません。")

    X = (x0 if a >= 0 else -x0) % abs(b)
    Y = (1 - a * X) // b

    return X, Y



# extended_euclid(a, b)  -> ax + by = 1を満たす特殊解(x,y)を返す
print(extended_euclid(11, 13)) # -> (6, -5)
print(extended_euclid(11,-13)) # -> (6,  5)

# 余談：特殊解(x, y) = (X, Y)を用いて，一般解は(x, y) = (-b*k + X, a*k + Y)  (kは整数)と表される
