#頂点s -> tへの最短経路を出力
def shortest_path(start, end, graph):
    import heapq as hq
    inf = 2 ** 61 - 1
    N = len(graph)
    heap = []
    dist = [inf] * N
    dist[start] = 0
    pre_nodes = [-1] * N
    hq.heappush(heap, (0, start))
    while heap:
        cnt, n = hq.heappop(heap)
        #重み０の辺がある場合はこれがいる
        if cnt > dist[n]:
            continue
        for k, w in graph[n]:
            if dist[n] + w >= dist[k]:
                continue
            dist[k] = dist[n] + w
            pre_nodes[k] = n
            hq.heappush(heap, (dist[n] + w, k))

    #到達不可能な場合、distと空配列を返す
    if dist[end] == inf:
        return dist, []
    
    rtn = []
    now = end
    while 1:
        rtn.append(now)
        if now == start:
            break
        now = pre_nodes[now]
    rtn = rtn[::-1]

    return dist, rtn




#yosupo_judge

N, M, s, t = map(int,input().split())
g = [[] for _ in range(N)]
for _ in range(M):
    a, b, c = map(int,input().split())
    g[a].append((b, c))


dist, path = shortest_path(s,t, g)
if dist[t] == 2 ** 61 - 1:
    print(-1)
    exit()
print(dist[t], len(path) - 1)
for i in range(len(path) - 1):
    print(path[i], path[i+1])

    
