def tree_dp(g: list):
    #0を根として、DP[i] (:頂点iを根とする部分木の何かのスコア)を返す
    #以下はABC220-F Distance Sum 2 より抜粋

    from collections import deque
    N = len(g)
    parent = [-1] * N   
    dist = []           #dist: 頂点0からの距離が遠い順に並んだノード
    d = deque()
    d.append([0,0])
    visited = [False] * N
    visited[0] = True
    while d:
        cnt, n = d.popleft()
        dist.append(n)
        for k in g[n]:
            if visited[k]:
                parent[n] = k
                continue
            d.append([cnt + 1, k])
            visited[k] = True
    dist.reverse()

    #この部分が部分木のマージ部分。変更可
    #以下は部分木の辺の数の総和とサイズを求める式

    treedist = [0]*N
    treesize = [1]*N
    for i in dist:
        if parent[i] == -1: continue
        treedist[parent[i]] += treedist[i] + treesize[i]
        treesize[parent[i]] += treesize[i]
    
    return treedist, treesize



def rerooting(N, G, merge, id_elem, put_edge, put_node):
    """
    全方位木DP (非再帰・左右からの累積和方式)
    
    :param N: 頂点数
    :param G: グラフ G[v] = [(u, weight), ...]
    :param merge: 2つの部分木の結果をマージする関数 merge(a, b)
    :param id_elem: マージの単位元（足し算なら0、maxなら-infなど）
    :param put_edge: 辺を通る時の変化の関数 put_edge(val, weight)
    :param put_node: 頂点を通る時の変化の関数 put_node(val, v)
    :return: 各頂点を根としたときのDP値の配列 ans
    """
    
    # 1. 根(頂点0)からのトポロジカル順序（行きがけ順）を取得 (BFS/DFS)
    order = []
    stack = [0]
    parents = [-1] * N
    while stack:
        v = stack.pop()
        order.append(v)
        for u, w in G[v]:
            if u != parents[v]:
                parents[u] = v
                stack.append(u)
    
    # 2. ボトムアップのDP (帰りがけ順)
    dp_v = [id_elem] * N
    for v in reversed(order):
        res = id_elem
        for u, w in G[v]:
            if u != parents[v]:
                res = merge(res, put_edge(dp_v[u], w))
        dp_v[v] = put_node(res, v)
    
    # 3. トップダウンのDP (行きがけ順)
    ans = [id_elem] * N
    dp_p = [id_elem] * N  # 親方向への部分木の答え
    
    for v in order:
        # vのすべての子（親も含む）からのDP値を集める
        adj_dp = []
        for u, w in G[v]:
            if u == parents[v]:
                adj_dp.append(put_edge(dp_p[v], w))
            else:
                adj_dp.append(put_edge(dp_v[u], w))
        
        # 答えの計算：全方向の値をマージする
        res = id_elem
        for val in adj_dp:
            res = merge(res, val)
        ans[v] = put_node(res, v)
        
        # 次のステップ（子へ配る）のために、左右からの累積和を計算
        deg = len(G[v])
        left = [id_elem] * (deg + 1)
        right = [id_elem] * (deg + 1)
        for i in range(deg):
            left[i + 1] = merge(left[i], adj_dp[i])
        for i in range(deg - 1, -1, -1):
            right[i] = merge(right[i + 1], adj_dp[i])
        
        # 自分の子 u に対して、u 以外の全ての方向の計算結果を渡す
        for i, (u, w) in enumerate(G[v]):
            if u != parents[v]:
                # u を除いた左右の累積和をマージ
                val = merge(left[i], right[i + 1])
                dp_p[u] = put_node(val, v)
                
    return ans