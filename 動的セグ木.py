# 配列A (|A|<1e9, max(A)<1e9)に対して一点更新，区間和取得ができる
# 最初はすべて0で初期化する

class TrueDynamicSegmentTree:
    def __init__(self, max_idx=10**9, initial_nodes=1000000):
        """
        max_idx       : インデックスの最大値 (例: 10^9 なら 0 ~ 10^9 の区間を管理)
        initial_nodes : 最初に確保しておくノード数 (PyPyの高速化のため)
        """
        self.max_idx = max_idx
        self.root = 1
        
        # PyPyでは array よりも標準の list のほうが高速
        self.left = [0] * initial_nodes
        self.right = [0] * initial_nodes
        self.sm = [0] * initial_nodes
        
        self.next_idx = 2
        self.current_values = {}

    def _reserve(self):
        """ノード配列が足りなくなった場合に動的に拡張する"""
        if self.next_idx >= len(self.left):
            extension_size = len(self.left)
            self.left.extend([0] * extension_size)
            self.right.extend([0] * extension_size)
            self.sm.extend([0] * extension_size)

    def update(self, idx, val):
        """
        インデックス idx の値を val に更新する (A[idx] = val)
        """
        # 変化量 (diff) を計算
        old_val = self.current_values.get(idx, 0)
        diff = val - old_val
        if diff == 0:
            return
            
        self.current_values[idx] = val
        
        # ローカル変数にキャッシュ
        left = self.left
        right = self.right
        sm = self.sm
        
        node = self.root
        l, r = 0, self.max_idx
        
        # 根に差分を足す
        sm[node] += diff
        
        # 葉に向かって降りながら更新
        while l < r:
            mid = (l + r) // 2
            
            if idx <= mid:
                # 左の子へ
                if not left[node]:
                    self._reserve()
                    # _reserve で再確保された場合、参照が変わる可能性があるため取得し直す
                    left = self.left
                    left[node] = self.next_idx
                    self.next_idx += 1
                node = left[node]
                r = mid
            else:
                # 右の子へ
                if not right[node]:
                    self._reserve()
                    right = self.right
                    right[node] = self.next_idx
                    self.next_idx += 1
                node = right[node]
                l = mid + 1
            
            sm[node] += diff

    def query(self, a, b):
        """
        区間 [a, b] の総和を返す (閉区間)
        再帰呼び出しによる関数コールのオーバーヘッドを防ぐため、スタックで非再帰実装
        """
        if a > b:
            return 0
            
        ans = 0
        # stack には (node, 現在の区間の左端, 現在の区間の右端) を積む
        stack = [(self.root, 0, self.max_idx)]
        
        # ローカル変数キャッシュ
        left = self.left
        right = self.right
        sm = self.sm
        
        while stack:
            node, l, r = stack.pop()
            
            # ノードが存在しない、またはクエリ区間と完全に交差しない場合
            if not node or b < l or r < a:
                continue
                
            # 現在の区間がクエリ区間に完全に内包されている場合
            if a <= l and r <= b:
                ans += sm[node]
                continue
                
            mid = (l + r) // 2
            
            # 子ノードをスタックに追加 (左を後に積むと、左から先に処理される)
            stack.append((right[node], mid + 1, r))
            stack.append((left[node], l, mid))
            
        return ans


# --- 動作確認 ---
if __name__ == "__main__":
    # max_idx は取りうる最大のインデックス
    # 今回は |A| < 5e5 なので、十分な大きさを持たせる
    dst = TrueDynamicSegmentTree(max_idx=500000)
    
    # 初期状態はすべて 0
    # A[10] = 5, A[20] = 15, A[30] = 10 に更新
    dst.update(10, 5)
    dst.update(20, 15)
    dst.update(30, 10)
    
    print(f"Sum [0, 15]   : {dst.query(0, 15)}")   # A[10] = 5
    print(f"Sum [15, 30]  : {dst.query(15, 30)}")  # A[20] + A[30] = 25
    print(f"Sum [0, 500]  : {dst.query(0, 500)}")  # 5 + 15 + 10 = 30
    
    # A[20] を 100 に一点更新 (上書き)
    dst.update(20, 100)
    print(f"Sum [0, 500] after update: {dst.query(0, 500)}") # 5 + 100 + 10 = 115