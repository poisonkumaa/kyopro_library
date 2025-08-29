class euler_tour:
    # できること
    # 任意の二点間の距離の取得               :      O(log N)
    # 任意の二点のLCA(最小共通祖先)の取得     :     O(log N)
    # 辺の重さ更新                          :     O(log N)
    # 任意の頂点を根とする部分木の辺の総和取得:      O(log N)


    #木gに対して、根を頂点0として
    # visit       : 頂点0からDFSして通った頂点の列
    # depth       : 頂点0からDFSして通った頂点の深さ
    # dist_tour   : 頂点0からDFSして通った辺の重み(上りなら負)
    # first_visit : 各頂点iに初めて訪れた時刻
    # last_visit  : 各頂点iに最後に訪れた時刻

    # 再帰禁止 (Pypyの再帰オーバーヘッド回避)


    def __init__(self, g, root = 0):
        self.N = len(g)
        self.g = g
        self.visit = []
        self.depth = []
        self.dist_tour = [] 
        self.first_visit = [-1] * self.N
        self.last_visit = [-1] * self.N
        self.edge_weights_for_subtree = [0] * (2 * self.N)

        self.parent = [-1] * self.N
        self.edge_to_parent_weight = {} 

        #非再帰DFS
        self.build_tour(root, -1, 0 , 0)

        for i , v in enumerate(self.visit):
            if self.first_visit[v] == -1:
                self.first_visit[v] = i
            self.last_visit[v] = i

        self.tour_depth = [(self.depth[i], self.visit[i]) for i in range(len(self.visit))]
        self.seg = SegTree_RMQ(self.tour_depth)

        self.dist_bit = FenwickTree(self.dist_tour)
        self.subtree_cost_bit = FenwickTree(self.edge_weights_for_subtree)


    def build_tour(self, root, root_parent, root_depth, root_weight):
        
        stack = [(root, root_parent, root_depth, root_weight)]
    
        g_iter = [iter(self.g[i]) for i in range(self.N)]

        # 行きがけ
        self.parent[root] = root_parent
        self.visit.append(root)
        self.depth.append(root_depth)
        self.dist_tour.append(root_weight)

        while stack:
            v, p, d, weight_to_v = stack[-1] # スタックの先頭を pop せずに見る

            found_child = False
            for neighbor, weight in g_iter[v]:
                if neighbor == p:
                    continue
                
                # 子の「行きがけ」処理
                self.parent[neighbor] = v
                self.edge_to_parent_weight[neighbor] = weight
                self.visit.append(neighbor)
                self.depth.append(d + 1)
                self.dist_tour.append(weight)
                self.edge_weights_for_subtree[len(self.visit) - 1] = weight

                stack.append((neighbor, v, d + 1, weight))
                
                found_child = True
                break 
            
            # --- 全ての子を探索し終わった場合 (再帰からのリターンに相当) ---
            if not found_child:
                stack.pop() 
                
                # 根でなければ、帰りがけ
                if p != -1:
                    self.visit.append(p)
                    self.depth.append(d - 1)
                    self.dist_tour.append(-weight_to_v)
            

    def LCA(self, u, v):
        # 頂点uとvの最小共通祖先を返す
        left = min(self.first_visit[u], self.first_visit[v])
        right = max(self.first_visit[u], self.first_visit[v])
        _, lca_node = self.seg.query(left, right + 1)
        return lca_node
    
    def dist_from_root(self, u):
        # 根から頂点uへの距離を返す
        return self.dist_bit.query(self.first_visit[u] + 1)
    
    def dist(self, u, v):
        # 頂点uとvの距離を返す
        l = self.LCA(u, v)
        dist_u = self.dist_from_root(u)
        dist_v = self.dist_from_root(v)
        dist_l = self.dist_from_root(l)
        return dist_u + dist_v - 2 * dist_l
    
    def get_subtree_edge_cost(self, x):
        #頂点xを根とする部分木に含まれる辺のコストの合計を計算
        start_idx = self.first_visit[x] + 1
        end_idx = self.last_visit[x] + 1

        if start_idx >= end_idx:
            return 0

        cost = self.subtree_cost_bit.query(end_idx) - self.subtree_cost_bit.query(start_idx)
        return cost
    
    def update_edge(self, u, v, new_weight):
        # 辺 (u, v) の重みを new_weight に更新する。
        if self.parent[v] == u:
            p, c = u, v
        elif self.parent[u] == v:
            p, c = v, u
        else:
            # u, v は親子関係にない場合
            raise ValueError(f"Edge ({u}, {v}) does not exist or is not a direct parent-child edge.")

        old_weight = self.edge_to_parent_weight[c]
        diff = new_weight - old_weight
        
        self.dist_bit.add(self.first_visit[c], diff)
        if self.last_visit[c] + 1 < self.dist_bit.n:
            self.dist_bit.add(self.last_visit[c] + 1, -diff)
        
        self.subtree_cost_bit.add(self.first_visit[c], diff)
        
        self.edge_to_parent_weight[c] = new_weight

    

class SegTree_RMQ:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1 << (self.n - 1).bit_length()
        self.tree = [(2 ** 61 - 1, -1)] * (2 * self.size)
        self._build(data)

    def _build(self, data):
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, l, r):
        res = (2 ** 61 - 1, -1)
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                res = min(res, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                res = min(res, self.tree[r])
            l >>= 1
            r >>= 1
        return res
    

class FenwickTree:
    def __init__(self, n_or_data):
        if isinstance(n_or_data, int):
            self.n = n_or_data
            self.data = [0] * self.n
        else:
            self.n = len(n_or_data)
            self.data = list(n_or_data)
            for i in range(1, self.n + 1):
                p = i + (i & -i)
                if p <= self.n:
                    self.data[p - 1] += self.data[i - 1]

    def add(self, i, x):
        #位置 i に x を加算する 
        i += 1
        while i <= self.n:
            self.data[i - 1] += x
            i += i & -i

    def query(self, i):
        #半開区間 [0, i) の和を求める
        res = 0
        while i > 0:
            res += self.data[i - 1]
            i -= i & -i
        return res
