from collections import deque

def topological_sort(g,indegree):
    N = len(g)
    #トポロジカルソートを返す配列
    L = []   
    #入次数が0の頂点のリストS
    #Sの取り出し方で得られる答えは異なってくるex)S = SortedListなど
    S = deque()
    for i in range(N):
        if indegree[i] == 0:
            S.append(i)

    #キューが空になるまで以下を繰り返す。
    while S:
        #キューの先頭を取り出す
        n = S.popleft()
        
        #その頂点と隣接している頂点の入次数を減らし、0になればキューに追加
        for k in g[n]:
            indegree[k] -= 1
            if indegree[k] == 0:
                S.append(k)
        L.append(n)
    
    return L
