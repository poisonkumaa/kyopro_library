import sys
import gc

# 配列Aに対して一点更新，上位K個，下位K個の総和を求める
# メモリに余裕があり、速度を最優先する場合
# プログラム開始時にGCを止めることで、実行中のメモリ解放のフリーズを防ぐ
gc.disable()

class FastDynamicSegmentTree:
    def __init__(self, init_array, max_value=10**9, max_nodes=None):
        # 10^9 なら 30ビットで表現可能
        self.MAX_LOG = max_value.bit_length()
        
        N = len(init_array)
        self.A = list(init_array)
        
        # 必要なノード数を見積もる (N + Q) * MAX_LOG + α
        if max_nodes is None:
            # 例: N=400,000, Q=200,000 を想定
            max_nodes = N * self.MAX_LOG + 200000 * self.MAX_LOG + 100
            
        # 【極限最適化 1】leftとrightを単一の配列に統合（キャッシュヒット率向上）
        # ch[node << 1] が左の子 (bit=0), ch[(node << 1) | 1] が右の子 (bit=1)
        self.ch = [0] * (max_nodes * 2)
        self.cnt = [0] * max_nodes
        self.sm = [0] * max_nodes
        
        self.next_idx = 2
        
        ch = self.ch
        cnt = self.cnt
        sm = self.sm
        MAX_LOG = self.MAX_LOG
        
        for val in self.A:
            node = 1
            cnt[node] += 1
            sm[node] += val
            for b in range(MAX_LOG - 1, -1, -1):
                bit = (val >> b) & 1
                idx = (node << 1) | bit
                nxt = ch[idx]
                if not nxt:
                    nxt = self.next_idx
                    self.next_idx += 1
                    ch[idx] = nxt
                node = nxt
                cnt[node] += 1
                sm[node] += val

    def update(self, idx, val):
        old_val = self.A[idx]
        if old_val == val:
            return
        self.A[idx] = val
        
        ch = self.ch
        cnt = self.cnt
        sm = self.sm
        MAX_LOG = self.MAX_LOG
        
        # --- 古い値の削除 (-1) ---
        node = 1
        cnt[node] -= 1
        sm[node] -= old_val
        for b in range(MAX_LOG - 1, -1, -1):
            bit = (old_val >> b) & 1
            node = ch[(node << 1) | bit]
            cnt[node] -= 1
            sm[node] -= old_val

        # --- 新しい値の追加 (+1) ---
        node = 1
        cnt[node] += 1
        sm[node] += val
        for b in range(MAX_LOG - 1, -1, -1):
            bit = (val >> b) & 1
            idx = (node << 1) | bit
            nxt = ch[idx]
            if not nxt:
                nxt = self.next_idx
                self.next_idx += 1
                ch[idx] = nxt
            node = nxt
            cnt[node] += 1
            sm[node] += val

    def query(self, k):
        """上位 K 個の総和を返す"""
        if k <= 0: return 0
        cnt = self.cnt
        sm = self.sm
        ch = self.ch
        
        if k >= cnt[1]:
            return sm[1]
            
        ans = 0
        node = 1
        val_acc = 0
        for b in range(self.MAX_LOG - 1, -1, -1):
            # 右の子(大きい値)のインデックス
            r_child = ch[(node << 1) | 1]
            
            # 【極限最適化 2】0番インデックスは常に0なので、if nullチェックが不要
            r_cnt = cnt[r_child]
            
            if k <= r_cnt:
                node = r_child
                val_acc |= (1 << b)
            else:
                ans += sm[r_child]
                k -= r_cnt
                node = ch[node << 1]
                
        if k > 0:
            ans += k * val_acc
        return ans

    def query_bottom(self, k):
        """下位 K 個の総和を返す"""
        if k <= 0: return 0
        cnt = self.cnt
        sm = self.sm
        ch = self.ch
        
        if k >= cnt[1]:
            return sm[1]
            
        ans = 0
        node = 1
        val_acc = 0
        for b in range(self.MAX_LOG - 1, -1, -1):
            # 左の子(小さい値)のインデックス
            l_child = ch[node << 1]
            l_cnt = cnt[l_child]
            
            if k <= l_cnt:
                node = l_child
            else:
                ans += sm[l_child]
                k -= l_cnt
                node = ch[(node << 1) | 1]
                val_acc |= (1 << b)
                
        if k > 0:
            ans += k * val_acc
        return ans
    
"""
N, M, Q = mi()
A = li()
B = li()
all = A + B
seg = FastDynamicSegmentTree(all)

q = [tuple(mi()) for _ in range(Q)]
out = []
for t,i,x in q:
    i -= 1
    if t == 2:
        i += N
    seg.update(i, x)
    out.append(str(seg.query(N//2) + seg.query_bottom(N//2)))
sys.stdout.write("\n".join(out) + "\n")
"""