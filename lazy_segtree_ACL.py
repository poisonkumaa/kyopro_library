#ACL,local対応
#inf = 2 ** 61 - 1を使用することで高速化

import typing
inf = 2 ** 61 - 1
def _ceil_pow2(n: int) -> int:
    x = 0
    while (1 << x) < n:
        x += 1

    return x

class LazySegTree:
    def __init__(
            self,
            op: typing.Callable[[typing.Any, typing.Any], typing.Any],
            e: typing.Any,
            mapping: typing.Callable[[typing.Any, typing.Any], typing.Any],
            composition: typing.Callable[[typing.Any, typing.Any], typing.Any],
            id_: typing.Any,
            v: typing.Union[int, typing.List[typing.Any]]) -> None:
        self._op = op
        self._e = e
        self._mapping = mapping
        self._composition = composition
        self._id = id_

        if isinstance(v, int):
            v = [e] * v

        self._n = len(v)
        self._log = _ceil_pow2(self._n)
        self._size = 1 << self._log
        self._d = [e] * (2 * self._size)
        self._lz = [self._id] * self._size
        for i in range(self._n):
            self._d[self._size + i] = v[i]
        for i in range(self._size - 1, 0, -1):
            self._update(i)

    def set(self, p: int, x: typing.Any) -> None:
        assert 0 <= p < self._n

        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        self._d[p] = x
        for i in range(1, self._log + 1):
            self._update(p >> i)

    def get(self, p: int) -> typing.Any:
        assert 0 <= p < self._n

        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        return self._d[p]

    def prod(self, left: int, right: int) -> typing.Any:
        assert 0 <= left <= right <= self._n

        if left == right:
            return self._e

        left += self._size
        right += self._size

        for i in range(self._log, 0, -1):
            if ((left >> i) << i) != left:
                self._push(left >> i)
            if ((right >> i) << i) != right:
                self._push((right - 1) >> i)

        sml = self._e
        smr = self._e
        while left < right:
            if left & 1:
                sml = self._op(sml, self._d[left])
                left += 1
            if right & 1:
                right -= 1
                smr = self._op(self._d[right], smr)
            left >>= 1
            right >>= 1

        return self._op(sml, smr)

    def all_prod(self) -> typing.Any:
        return self._d[1]

    def apply(self, left: int, right: typing.Optional[int] = None,
              f: typing.Optional[typing.Any] = None) -> None:
        assert f is not None

        if right is None:
            p = left
            assert 0 <= left < self._n

            p += self._size
            for i in range(self._log, 0, -1):
                self._push(p >> i)
            self._d[p] = self._mapping(f, self._d[p])
            for i in range(1, self._log + 1):
                self._update(p >> i)
        else:
            assert 0 <= left <= right <= self._n
            if left == right:
                return

            left += self._size
            right += self._size

            for i in range(self._log, 0, -1):
                if ((left >> i) << i) != left:
                    self._push(left >> i)
                if ((right >> i) << i) != right:
                    self._push((right - 1) >> i)

            l2 = left
            r2 = right
            while left < right:
                if left & 1:
                    self._all_apply(left, f)
                    left += 1
                if right & 1:
                    right -= 1
                    self._all_apply(right, f)
                left >>= 1
                right >>= 1
            left = l2
            right = r2

            for i in range(1, self._log + 1):
                if ((left >> i) << i) != left:
                    self._update(left >> i)
                if ((right >> i) << i) != right:
                    self._update((right - 1) >> i)

    def max_right(
            self, left: int, g: typing.Callable[[typing.Any], bool]) -> int:
        assert 0 <= left <= self._n
        assert g(self._e)

        if left == self._n:
            return self._n

        left += self._size
        for i in range(self._log, 0, -1):
            self._push(left >> i)

        sm = self._e
        first = True
        while first or (left & -left) != left:
            first = False
            while left % 2 == 0:
                left >>= 1
            if not g(self._op(sm, self._d[left])):
                while left < self._size:
                    self._push(left)
                    left *= 2
                    if g(self._op(sm, self._d[left])):
                        sm = self._op(sm, self._d[left])
                        left += 1
                return left - self._size
            sm = self._op(sm, self._d[left])
            left += 1

        return self._n

    def min_left(self, right: int, g: typing.Any) -> int:
        assert 0 <= right <= self._n
        assert g(self._e)

        if right == 0:
            return 0

        right += self._size
        for i in range(self._log, 0, -1):
            self._push((right - 1) >> i)

        sm = self._e
        first = True
        while first or (right & -right) != right:
            first = False
            right -= 1
            while right > 1 and right % 2:
                right >>= 1
            if not g(self._op(self._d[right], sm)):
                while right < self._size:
                    self._push(right)
                    right = 2 * right + 1
                    if g(self._op(self._d[right], sm)):
                        sm = self._op(self._d[right], sm)
                        right -= 1
                return right + 1 - self._size
            sm = self._op(self._d[right], sm)

        return 0

    def _update(self, k: int) -> None:
        self._d[k] = self._op(self._d[2 * k], self._d[2 * k + 1])

    def _all_apply(self, k: int, f: typing.Any) -> None:
        self._d[k] = self._mapping(f, self._d[k])
        if k < self._size:
            self._lz[k] = self._composition(f, self._lz[k])

    def _push(self, k: int) -> None:
        self._all_apply(2 * k, self._lz[k])
        self._all_apply(2 * k + 1, self._lz[k])
        self._lz[k] = self._id


#========================================================
#区間加算・区間最大値取得

INF = inf

# 値の2項演算
def op(value1, value2):
    return max(value1, value2)

# 上のブロックの作用素を下のブロックの値に伝播
def mapping(f, value):
    return f + value

# 上のブロックの作用素を下のブロックの作用素に伝播
def composition(f, g):
    return f + g

# 値の単位元
e = -INF

# 作用素の単位元
id_ = 0

l = [0,1,2,3,4,5,6]
LST = LazySegTree(op, e, mapping, composition, id_, l)

#========================================================
#区間更新・区間最大値取得

# 値の2項演算
def op(value1, value2):
    return max(value1, value2)

# 上のブロックの作用素を下のブロックの値に伝播
def mapping(f, value):
    return value if f is id_ else f

# 上のブロックの作用素を下のブロックの作用素に伝播
def composition(f, g):
    return g if f is id_ else f

# 値の単位元
e = -inf

# 作用素の単位元
id_ = None

l = [0,1,2,3,4,5,6]
LST = LazySegTree(op, e, mapping, composition, id_, l)

#========================================================
#区間加算・区間最小値

INF = inf

# 値の2項演算
def op(value1, value2):
    return min(value1, value2)

# 上のブロックの作用素を下のブロックの値に伝播
def mapping(f, value):
    return f + value

# 上のブロックの作用素を下のブロックの作用素に伝播
def composition(f, g):
    return f + g

# 値の単位元
e = INF

# 作用素の単位元
id_ = 0

l = [0,1,2,3,4,5,6]
LST = LazySegTree(op, e, mapping, composition, id_, l)

#========================================================
#区間更新・区間最小値

# 値の2項演算
def op(value1, value2):
    return min(value1, value2)

# 上のブロックの作用素を下のブロックの値に伝播
def mapping(f, value):
    return value if f is id_ else f

# 上のブロックの作用素を下のブロックの作用素に伝播
def composition(f, g):
    return g if f is id_ else f

# 値の単位元
e = inf

# 作用素の単位元
id_ = None

l = [0,1,2,3,4,5,6]
LST = LazySegTree(op, e, mapping, composition, id_, l)

#========================================================
#区間加算・区間和取得

# 値の2項演算
def op(value1, value2):
    return [value1[0]+value2[0],value1[1]+value2[1]]

# 上のブロックの作用素を下のブロックの値に伝播
def mapping(f, value):
    return [value[0],value[1]+f*value[0]]

# 上のブロックの作用素を下のブロックの作用素に伝播
def composition(f, g):
    return f+g

# 値の単位元
e = [0,0]

# 作用素の単位元
id_ = 0

l = [0,1,2,3,4,5,6]

# 区間和取得の場合は[区間のサイズ, 値]として扱う
l = [[1,value] for value in l]
LST = LazySegTree(op, e, mapping, composition, id_, l)

#======================================================================
# 区間加算，0,1,2乗区間和取得
mod = 998244353

def op(x, y):
    z = [0, 0, 0]
    z[0] = x[0] + y[0]
    z[1] = (x[1] + y[1]) % mod
    z[2] = (x[2] + y[2]) % mod
    
    return z
E = [0, 0, 0]

def mapping(f, x):
    z = [0, 0, 0]
    z[0] = x[0]
    z[1] = (x[1] + f * x[0]) % mod
    z[2] = (x[2] + 2 * x[1] * f + x[0] * f % mod * f) % mod
    return z

def composition(f, g):
    return f + g
    
N = int(input())
seg = LazySegTree(op, E, mapping, composition, 0, [[1, 0, 0] for _ in range(N)])

#========================================================
#区間更新・区間和取得

# 値の2項演算
def op(value1, value2):
    return [value1[0]+value2[0],value1[1]+value2[1]]

# 上のブロックの作用素を下のブロックの値に伝播
def mapping(f, value):
    if f is id_:return value
    return [value[0],f*value[0]]

# 上のブロックの作用素を下のブロックの作用素に伝播
def composition(f, g):
    return g if f is id_ else f

# 値の単位元
e = [0,0]

# 作用素の単位元
id_ = None

l = [0,1,2,3,4,5,6]

# 区間和取得の場合は[区間のサイズ, 値]として扱う
l = [[1,value] for value in l]
LST = LazySegTree(op, e, mapping, composition, id_, l)


########使用例########################################################################
l = [0,1,2,3,4,5,6]
l = [[1,value] for value in l]  
LST = LazySegTree(op, e, mapping, composition, id_, l)

# [2,5)を3で更新
LST.apply(2,5,3) # [0,1,3,3,3,5,6]

#返り値は[要素数, 値]となる

# 区間の演算結果を取得
print(LST.prod(2,5)) # [3,9]
print(LST.prod(3,7)) # [4,17]

# LST.prod(left, x)がgを満たす最大のxを二分探索
left = 0
g = lambda x: x[1]<15
print(LST.max_right(left , g)) # 5

#i = 2を4に更新
LST.set(2, [1, 4])   



#========================================================
