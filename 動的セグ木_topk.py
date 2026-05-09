# 配列Aについて、一点更新、上位K個の総和を高速に計算できる
# |A| < 5e5, A[i] < 1e9
# 初期化ー＞すべて0とする


from array import array

class FastDynamicSegmentTree:
    def __init__(self, max_value=10**9):
        self.max_val = max_value
        self.root = 1
        
        # ノード管理用の配列
        self.left = array('I', [0, 0])  # 左の子のインデックス
        self.right = array('I', [0, 0]) # 右の子のインデックス
        self.cnt = array('I', [0, 0])   # 部分木の要素数
        self.sm = array('q', [0, 0])    # 部分木の総和
        
        # 次に割り当てるノードのインデックス
        self.next_idx = 2
        
        # 現在の配列Aの値を保持 (一点更新のため)
        # Aのインデックス -> 値
        self.current_values = {}

    def _reserve(self):
        if self.next_idx >= len(self.left):
            # 現在の長さ分だけ拡張
            extension_size = len(self.left)
            self.left.extend(array('I', [0] * extension_size))
            self.right.extend(array('I', [0] * extension_size))
            self.cnt.extend(array('I', [0] * extension_size))
            self.sm.extend(array('q', [0] * extension_size))

    def update(self, idx, val):
        """
        配列Aのインデックス idx を val に更新する
        """
        # 1. 以前の値があれば取り消す (-1)
        if idx in self.current_values:
            old_val = self.current_values[idx]
            if old_val == val:
                return
            self._add(old_val, -1)
        
        # 2. 新しい値を追加する (+1)
        self.current_values[idx] = val
        self._add(val, 1)

    def _add(self, val, diff_cnt):
        """
        内部メソッド: val の位置に diff_cnt (+1 or -1) を加算
        Iterative (非再帰) 実装
        """
        node = self.root
        l, r = 0, self.max_val
        diff_sum = val * diff_cnt
        
        # 根の情報を更新
        self.cnt[node] += diff_cnt
        self.sm[node] += diff_sum
        
        while l < r:
            mid = (l + r) // 2
            
            # 行き先 (0:左, 1:右)
            if val <= mid:
                # 左の子へ
                if not self.left[node]:
                    self._reserve()
                    self.left[node] = self.next_idx
                    self.next_idx += 1
                node = self.left[node]
                r = mid
            else:
                # 右の子へ
                if not self.right[node]:
                    self._reserve()
                    self.right[node] = self.next_idx
                    self.next_idx += 1
                node = self.right[node]
                l = mid + 1
            
            # パス上のノードを更新 (戻りがけの計算は不要、降りながら足すだけ)
            self.cnt[node] += diff_cnt
            self.sm[node] += diff_sum

    def query(self, k):
        """
        上位 K 個の総和を返す
        Iterative (非再帰) 実装
        """
        if k <= 0:
            return 0
        
        node = self.root
        
        # 全体数よりKが大きい場合は全合計を返す
        if k >= self.cnt[node]:
            return self.sm[node]
        
        l, r = 0, self.max_val
        ans = 0
        
        while l < r:
            mid = (l + r) // 2
            
            # 右側（大きい値側）の子を見る
            r_child = self.right[node]
            
            # 右側の子にいくつあるか
            r_cnt = self.cnt[r_child] if r_child else 0
            
            if k <= r_cnt:
                # 上位K個はすべて右側に収まる -> 右へ移動
                node = r_child
                l = mid + 1
            else:
                # 右側をすべて採用し、残りを左側で探す
                r_sum = self.sm[r_child] if r_child else 0
                ans += r_sum
                k -= r_cnt
                
                # 左へ移動
                node = self.left[node]
                r = mid
                
                # 左の子がない場合（通常ここには来ないが安全策）
                if not node:
                    break
        
        # 葉に到達した場合 (l == r)
        if l == r and k > 0:
            ans += l * k
            
        return ans
    


# --- 動作確認 ---
if __name__ == "__main__":
    import time
    
    # 簡単なテスト
    dst = FastDynamicSegmentTree(max_value=10**9)
    
    # A = [10, 20, 5, 30]
    dst.update(0, 10)
    dst.update(1, 20)
    dst.update(2, 5)
    dst.update(3, 30)
    
    # Top 2 sum -> 30 + 20 = 50
    print(f"Top 2 sum: {dst.query(2)}") 
    
    # Update A[2] 5 -> 100
    dst.update(2, 100)
    # A = [10, 20, 100, 30]
    
    # Top 3 sum -> 100 + 30 + 20 = 150
    print(f"Top 3 sum: {dst.query(3)}")