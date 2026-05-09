#頂点startからの各頂点への最短距離(重さ0の辺ok)

def dijkkstra(start, graph):
    import heapq as hq
    inf = 2 ** 61 - 1
    N = len(graph)
    heap = []
    dist = [inf] * N
    dist[start] = 0
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
            hq.heappush(heap, (dist[n] + w, k))
    
    return dist

