#startからendまでの最短経路を返す関数
#g[i] = [[j,num]...]とする必要がある
def find_shortest_path_edges(start, end, g):
    from collections import deque
    # 始点と終点が同じ場合は、通る辺はないので空のリストを返す
    if start == end:
        return []
    queue = deque([(start, [])])
    visited = {start}

    while queue:
        current_vertex, path_edges = queue.popleft()

        # 現在の頂点に接続されている辺を調べる
        # グラフのサイズを超えた頂点番号の場合はスキップ
        if current_vertex >= len(g):
            continue
            
        for neighbor, edge_number in g[current_vertex]:
            # 未訪問の頂点であれば処理を行う
            if neighbor not in visited:
                new_path_edges = path_edges + [edge_number]
                
                # 目的の頂点に到達した場合
                if neighbor == end:
                    return new_path_edges # 最短経路の辺番号リストを返す
                
                # 訪問済みとしてマークし、キューに追加
                visited.add(neighbor)
                queue.append((neighbor, new_path_edges))

    # キューが空になっても終点に到達しなかった場合、経路は存在しない
    return []
