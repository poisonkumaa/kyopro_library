import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline
#再帰なのでCpythonの方が早い説がある(pair of ballsなど)

def has_cycle(adj, N):
    """
    adj: 隣接リスト（0-indexed）
    N: 頂点数
    return: サイクルがあれば True、なければ False
    """
    color = [0] * N  
    # color[u] = 0: 未訪問
    #            1: 探索中（現在の再帰スタック上）
    #            2: 完全に探索済み

    def dfs(u):
        color[u] = 1
        for v in adj[u]:
            if color[v] == 0:
                if dfs(v):
                    return True
            elif color[v] == 1:
                # 探索中の頂点に戻る辺がある ⇒ サイクル
                return True
        color[u] = 2
        return False

    for u in range(N):
        if color[u] == 0:
            if dfs(u):
                return True
    return False

"""
def main():
    N, M = map(int, input().split())
    adj = [[] for _ in range(N)]
    for _ in range(M):
        u, v = map(int, input().split())
        # 頂点番号が 1 〜 N ならば 0-index に直す
        adj[u-1].append(v-1)

    if has_cycle(adj, N):
        print("Yes")  # サイクルあり
    else:
        print("No")   # サイクルなし

if __name__ == "__main__":
    main()
"""