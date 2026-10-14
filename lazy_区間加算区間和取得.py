class RangeAddQueryBIT:
    """
    0-indexed, 半開区間 [l, r) に対する区間加算・区間和取得
    BITを2本用いることで遅延セグメント木より高速に動作する
    """
    def __init__(self, A):
        self.n = len(A)
        self.bit0 = [0] * (self.n + 2)
        self.bit1 = [0] * (self.n + 2)
        
        for i, a in enumerate(A):
            if a == 0: continue
            l, r = i + 1, i + 2
            self.bit0[l] -= (l - 1) * a
            self.bit1[l] += a
            self.bit0[r] += (r - 1) * a
            self.bit1[r] -= a
            
        for i in range(1, self.n + 1):
            nxt = i + (i & -i)
            if nxt <= self.n + 1:
                self.bit0[nxt] += self.bit0[i]
                self.bit1[nxt] += self.bit1[i]

    def add(self, l, r, x):
        """ 区間 [l, r) に x を加算 """
        if x == 0 or l >= r: return
        
        # l の位置への加算
        L = l + 1
        v0 = -(L - 1) * x
        v1 = x
        while L <= self.n:
            self.bit0[L] += v0
            self.bit1[L] += v1
            L += L & -L
            
        # r の位置への減算
        R = r + 1
        v0 = (R - 1) * x
        v1 = -x
        while R <= self.n:
            self.bit0[R] += v0
            self.bit1[R] += v1
            R += R & -R

    def _prefix_sum(self, i):
        s0, s1 = 0, 0
        idx = i
        while idx > 0:
            s0 += self.bit0[idx]
            s1 += self.bit1[idx]
            idx -= idx & -idx
        return s0 + s1 * i

    def sum(self, l, r):
        """ 区間 [l, r) の和を取得 """
        if l >= r: return 0
        return self._prefix_sum(r) - self._prefix_sum(l)
