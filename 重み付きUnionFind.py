from typing import Callable, Generic, TypeVar, List
 
T = TypeVar('T')
 
class UnionFindWithPotential(Generic[T]):
 
    def __init__(self,
                 n: int,
                 init: Callable[[], T],
                 func: Callable[[T, T], T],
                 rev_func: Callable[[T, T], T]):
        """
        :param n:
        :param init: 単位元の生成関数
        :param func: 2項間加算関数（add）
        :param rev_func: 逆関数（sub）
        """
        self.table: List[int] = [-1] * n
        self.values: List[T] = [init() for _ in range(n)]
        self.init: Callable[[], T] = init
        self.func: Callable[[T, T], T] = func
        self.rev_func: Callable[[T, T], T] = rev_func
 
    def root(self, x: int) -> int:
        stack = []
        tbl = self.table
        vals = self.values
 
        while tbl[x] >= 0:
            stack.append(x)
            x = tbl[x]
        if stack:
            val = self.init()
            while stack:
                y = stack.pop()
                val = self.func(val, vals[y])
                vals[y] = val
                tbl[y] = x
        return x
 
    def is_same(self, x: int, y: int) -> bool:
        return self.root(x) == self.root(y)
 
    def diff(self, x: int, y: int) -> T:
        """
        x と y の差（y - x）を取得。同じグループに属さない場合は None。
        """
        if not self.is_same(x, y):
            return None
        vx = self.values[x]
        vy = self.values[y]
        return self.rev_func(vy, vx)
 
    def unite(self, x: int, y: int, d: T) -> bool:
        """
        x と y のグループを、y - x = d となるように統合。
        既に x と y が同グループで、矛盾する場合は AssertionError。矛盾しない場合はFalse。
        同グループで無く、新たな統合が発生した場合はTrue。
        """
        rx = self.root(x)
        ry = self.root(y)
        vx = self.values[x]
        vy = self.values[y]
        if rx == ry:
            assert self.rev_func(vy, vx) == d
            return False
 
        rd = self.rev_func(self.func(vx, d), vy)
        self.table[rx] += self.table[ry]
        self.table[ry] = rx
        self.values[ry] = rd
        return True
 
    def get_size(self, x: int) -> int:
        return -self.table[self.root(x)]
    

"""
#初期化例
N = ii()


# 1.足し算、引き算

UF = UnionFindWithPotential[int](
    n=n,
    init=lambda: 0,                  
    func=lambda a, b: a + b,         
    rev_func=lambda a, b: a - b     
)

# 2.あまり(mod)つきの計算
# T = int で、mod 1000000007 を取る場合
MOD = 998244353
n = 10
UF = UnionFindWithPotential[int](
    n=n,
    init=lambda: 0,
    func=lambda a, b: (a + b) % MOD,
    rev_func=lambda a, b: (a - b) % MOD
)


# 3.XOR
n = 10
UF = UnionFindWithPotential[int](
    n=n,
    init=lambda: 0,                  # XORの単位元も 0
    func=lambda a, b: a ^ b,         # XOR
    rev_func=lambda a, b: a ^ b      # XORの逆演算はXOR自身
)


# 4.2次元タプル
from typing import Tuple

# T = Tuple[int, int] の場合
n = 10
UF = UnionFindWithPotential[Tuple[int, int]](
    n=n,
    init=lambda: (0, 0),                                # 原点
    func=lambda a, b: (a[0] + b[0], a[1] + b[1]),       # ベクトルの加算
    rev_func=lambda a, b: (a[0] - b[0], a[1] - b[1])    # ベクトルの減算
)

# 使用例: 点1から見て点2が x方向に+3, y方向に-4 の位置にある
uf_vec.unite(1, 2, (3, -4))

"""