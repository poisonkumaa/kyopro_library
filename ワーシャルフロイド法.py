
#ワーシャルフロイド法
#https://algo-logic.info/warshall-floyd/ 
#例題_ABC369_Eなど 
#
"""
ワーシャル・フロイド法：（「dist[ i ][ j ] := 頂点 i から j への最短経路」を求める）

dist[ i ][ j ] を以下のように初期化する
頂点 i から j へのコスト c(i, j) の辺がある時：dist[ i ][ j ] = c(i, j)
i = j の時：dist[ i ][ i ] = 0
上記以外の時：dist[ i ][ j ] = INF
dist を以下のように更新する
経由点 k = 0 から V-1 まで以下を行う
始点 i = 0 から V-1 まで以下を行う
終点 j = 0 から V-1 まで以下を行う
i →* k →* j という経路（dist[ i ][ k ] + dist[ k ][ j ]）が、dist[ i ][ j ] よりも小さければ更新

※ dist の更新は 3重の for ループを利用して、以下のように簡単に書くことができます。
※ k->i->j であることに注意！
for (int k = 0; k < V; k++) {
    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
        }
    }
}

3重の for ループを使うので、計算量は O(|V|3) になります。
"""