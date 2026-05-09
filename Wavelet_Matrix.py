import itertools
from typing import List

class BitVector:
    """簡潔ビットベクトル"""
    def __init__(self, n: int):
        self.n = n
        self.block = (n >> 5) + 1
        self.bit = [0] * self.block
        self.cnt = [0] * self.block
        self.zeros = 0

    def set(self, i: int) -> None:
        self.bit[i >> 5] |= 1 << (i & 31)

    def get(self, i: int) -> int:
        return (self.bit[i >> 5] >> (i & 31)) & 1

    def build(self) -> None:
        for i in range(self.block - 1):
            self.cnt[i + 1] = self.cnt[i] + self.popcount(self.bit[i])
        self.zeros = self.rank0(self.n)

    def popcount(self, x: int) -> int:
        x = x - ((x >> 1) & 0x55555555)
        x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
        x = (x + (x >> 4)) & 0x0f0f0f0f
        x = x + (x >> 8)
        x = x + (x >> 16)
        return x & 0x0000007f

    def rank1(self, i: int) -> int:
        mask = (1 << (i & 31)) - 1
        return self.cnt[i >> 5] + self.popcount(self.bit[i >> 5] & mask)

    def rank0(self, i: int) -> int:
        return i - self.rank1(i)


class WaveletMatrix:
    def __init__(self, A: List[int]):
        self.n = max(len(A), 1)
        
        # 値クエリ用の木
        self.lg_v = max(A + [1]).bit_length()
        self.b = [BitVector(self.n) for _ in range(self.lg_v)]
        self.sums = [None] * (self.lg_v + 1)
        self._build(A, self.b, self.lg_v, is_value_tree=True)

        # 種類数クエリ用の木
        prev_i = [0] * len(A)
        last_pos = {}
        for i, a in enumerate(A):
            prev_i[i] = last_pos.get(a, -1) + 1
            last_pos[a] = i
            
        self.lg_cnt = max(prev_i + [1]).bit_length()
        self.cnt = [BitVector(self.n) for _ in range(self.lg_cnt)]
        self._build(prev_i, self.cnt, self.lg_cnt, is_value_tree=False)

    def _build(self, arr: List[int], bv_list: List[BitVector], lg: int, is_value_tree: bool) -> None:
        if is_value_tree:
            # 構築前の元配列の累積和を最上層(lg_v)に保持
            self.sums[lg] = [0] + list(itertools.accumulate(arr))

        cur = arr[:]
        for h in range(lg - 1, -1, -1):
            bv = bv_list[h]
            bv_set = bv.set
            
            ls, rs = [], []
            ls_append, rs_append = ls.append, rs.append

            for i, val in enumerate(cur):
                if (val >> h) & 1:
                    bv_set(i)
                    rs_append(val)
                else:
                    ls_append(val)
            
            bv.build()
            cur = ls + rs
            
            if is_value_tree:
                self.sums[h] = [0] + list(itertools.accumulate(cur))

    # ====================================================
    # 1. 取得・検索系 (Access / Kth)
    # ====================================================
    def access(self, k: int) -> int:
        """k 番目 (0-indexed) の要素の値を返す"""
        ret = 0
        for h in range(self.lg_v - 1, -1, -1):
            f = self.b[h].get(k)
            if f:
                ret |= 1 << h
                k = self.b[h].rank1(k) + self.b[h].zeros
            else:
                k = self.b[h].rank0(k)
        return ret

    def kth_smallest(self, l: int, r: int, k: int) -> int:
        """区間 [l, r) の範囲で k 番目 (0-indexed) に小さい値を返す"""
        res = 0
        for h in range(self.lg_v - 1, -1, -1):
            l0 = self.b[h].rank0(l)
            r0 = self.b[h].rank0(r)
            if k < r0 - l0:
                l, r = l0, r0
            else:
                k -= r0 - l0
                res |= 1 << h
                l += self.b[h].zeros - l0
                r += self.b[h].zeros - r0
        return res

    def kth_largest(self, l: int, r: int, k: int) -> int:
        """区間 [l, r) の範囲で k 番目 (0-indexed) に大きい値を返す"""
        return self.kth_smallest(l, r, r - l - 1 - k)

    # ====================================================
    # 2. カウント・個数系 (Frequency / Count)
    # ====================================================
    def range_freq(self, l: int, r: int, upper: int) -> int:
        """区間 [l, r) の範囲で upper 未満の要素の個数を返す"""
        if upper >= (1 << self.lg_v):
            return r - l
        ret = 0
        for h in range(self.lg_v - 1, -1, -1):
            f = (upper >> h) & 1
            l0 = self.b[h].rank0(l)
            r0 = self.b[h].rank0(r)
            if f:
                ret += r0 - l0
                l += self.b[h].zeros - l0
                r += self.b[h].zeros - r0
            else:
                l, r = l0, r0
        return ret

    def range_freq_range(self, l: int, r: int, lower: int, upper: int) -> int:
        """区間 [l, r) の範囲で lower 以上 upper 未満の要素の個数を返す"""
        if lower >= upper: return 0
        return self.range_freq(l, r, upper) - self.range_freq(l, r, lower)

    def range_count(self, l: int, r: int) -> int:
        """区間 [l, r) の種類数 (Count Distinct) を返す"""
        upper = l + 1
        if upper >= (1 << self.lg_cnt):
            return r - l
        ret = 0
        for h in range(self.lg_cnt - 1, -1, -1):
            f = (upper >> h) & 1
            l0 = self.cnt[h].rank0(l)
            r0 = self.cnt[h].rank0(r)
            if f:
                ret += r0 - l0
                l += self.cnt[h].zeros - l0
                r += self.cnt[h].zeros - r0
            else:
                l, r = l0, r0
        return ret

    # ====================================================
    # 3. 前後探索系 (Predecessor / Successor)
    # ====================================================
    def prev_value(self, l: int, r: int, upper: int) -> int:
        """区間 [l, r) の範囲で upper 未満の最大の値を返す (存在しない場合は -1)"""
        cnt = self.range_freq(l, r, upper)
        return -1 if cnt == 0 else self.kth_smallest(l, r, cnt - 1)

    def next_value(self, l: int, r: int, lower: int) -> int:
        """区間 [l, r) の範囲で lower 以上の最小の値を返す (存在しない場合は -1)"""
        cnt = self.range_freq(l, r, lower)
        return -1 if cnt == r - l else self.kth_smallest(l, r, cnt)

    # ====================================================
    # 4. 総和系 (Sum) 
    # ====================================================
    def kth_sum(self, l: int, r: int, k: int) -> int:
        """区間 [l, r) を昇順ソートしたときの、先頭からk個の要素の「総和」を返す"""
        if k <= 0: return 0
        k = min(k, r - l)
        res_sum = 0
        val = 0
        for h in range(self.lg_v - 1, -1, -1):
            l0 = self.b[h].rank0(l)
            r0 = self.b[h].rank0(r)
            num0 = r0 - l0
            if num0 < k:
                res_sum += self.sums[h][r0] - self.sums[h][l0]
                k -= num0
                val |= 1 << h
                l += self.b[h].zeros - l0
                r += self.b[h].zeros - r0
            else:
                l, r = l0, r0
        # 最後に端数となったk個分の値を足す
        res_sum += k * val
        return res_sum

    def range_sum(self, l: int, r: int, mink: int, maxk: int) -> int:
        """区間 [l, r) の中で、値が mink 以上 maxk 未満である要素の「総和」を返す"""
        if mink >= maxk or l >= r:
            return 0
            
        def range_sum_upper(end_val: int) -> int:
            """区間内の end_val 未満の総和を計算する内部関数"""
            if end_val >= (1 << self.lg_v):
                return self.sums[self.lg_v][r] - self.sums[self.lg_v][l]
            res = 0
            cur_l, cur_r = l, r
            for h in range(self.lg_v - 1, -1, -1):
                f = (end_val >> h) & 1
                l0 = self.b[h].rank0(cur_l)
                r0 = self.b[h].rank0(cur_r)
                if f:
                    # 注目ビットが1なら、0のグループはすべて end_val 未満になるので総和を足す
                    res += self.sums[h][r0] - self.sums[h][l0]
                    cur_l += self.b[h].zeros - l0
                    cur_r += self.b[h].zeros - r0
                else:
                    cur_l, cur_r = l0, r0
            return res

        return range_sum_upper(maxk) - range_sum_upper(mink)
    


"""
# クエリなら以下のように入出力するとよい
q = [tuple(mi()) for _ in range(Q)]
out = []
for l, r in q:
    l -= 1        
    ans = wm.range_count(l, r)
    out.append(str(ans))

sys.stdout.write('\n'.join(out) + '\n')
"""