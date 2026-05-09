#by ABC361-E
#木の直径を求める方法：
#1: 頂点1から最も遠い点uを特定
#2: 頂点uから最も遠い点vを特定
#dist[u][v]が直径


#辺に重さがある場合
from collections import deque

N = int(input())
g = [[] for _ in range(N)]
SUMc = 0
for _ in range(N-1):
    a,b,c = map(int,input().split())
    a -= 1; b -= 1
    g[a].append([b,c])
    g[b].append([a,c])
    SUMc += c

def search(start):
    dist = [0] * N
    d = deque()
    d.append([start,0])  #node, cnt
    visited = [False] * N
    visited[start] = True
    while d:
        n, cnt = d.popleft()
        dist[n] = cnt
        for k, w in g[n]:
            if visited[k]:
                continue
            visited[k] = True
            d.append([k,cnt+w])
            
    ans_dist = 0
    ans_idx = -1
    for i in range(N):
        if dist[i] > ans_dist:
            ans_dist = dist[i]
            ans_idx = i
    return ans_idx, ans_dist




#辺に重さがない場合
from collections import deque

N = int(input())
g = [[] for _ in range(N)]
SUMc = 0
for _ in range(N-1):
    a,b = map(int,input().split())
    a -= 1; b -= 1
    g[a].append(b)
    g[b].append(a)

def search(start):
    dist = [0] * N
    d = deque()
    d.append([start,0])  #node, cnt
    visited = [False] * N
    visited[start] = True
    while d:
        n, cnt = d.popleft()
        dist[n] = cnt
        for k in g[n]:
            if visited[k]:
                continue
            visited[k] = True
            d.append([k,cnt+1])
        if not d:
            return n, cnt