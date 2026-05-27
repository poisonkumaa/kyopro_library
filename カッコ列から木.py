import sys

class BracketTreeParser:
    """
    文字列をパースし、0-indexedの隣接リスト（木）を構築する汎用ライブラリ
    頂点 0 を「仮想的な根（文字列全体）」とする。
    """
    def __init__(self, open_chars="([{", close_chars=")]}"):
        self.open_chars = set(open_chars)
        self.close_chars = set(close_chars)
        # 閉じ括弧から開き括弧を逆引きできるようにする
        self.pair = {c: o for c, o in zip(close_chars, open_chars)}

    def parse(self, tokens: str):
        """
        返り値: (G, vals)
        G: G[u] = [v1, v2, ...] (隣接リスト)
        vals: vals[u] = 頂点 u が持つ値（括弧の種類、または文字/数値）
        ※ 構文エラーの場合は (None, None) を返す
        """
        G = [[]]          # グラフ (頂点0は仮想根)
        vals = [None]     # 頂点の持つ値
        parent = [-1]     # 親への逆辺（構築用）
        curr = 0          # 現在着目している頂点番号

        for tk in tokens:
            if tk in self.open_chars:
                # 新しい階層（括弧）に入る
                new_node = len(G)
                G.append([])
                vals.append(tk)  # どの種類の括弧かを記録
                parent.append(curr)
                G[curr].append(new_node)
                curr = new_node
                
            elif tk in self.close_chars:
                # 階層（括弧）から抜ける
                # エラーチェック: 余分な閉じ括弧、または括弧の種類が不一致
                if curr == 0 or vals[curr] != self.pair[tk]:
                    return None, None
                curr = parent[curr]
                
            else:
                # 葉ノード（英字、数字、演算子など）
                new_node = len(G)
                G.append([])
                vals.append(tk)
                parent.append(curr)
                G[curr].append(new_node)

        # 最後に根に戻ってきていなければ、閉じ忘れがある（構文エラー）
        if curr != 0:
            return None, None

        return G, vals



S = "((XYZ)n(X(y)Z))"

parser = BracketTreeParser(open_chars="(", close_chars=")")
g, vals = parser.parse(S)
print(g, file=sys.stderr)
print(vals, file=sys.stderr)


# ABC350-Fにおけるdfs構築の例
ans = []
def dfs(i, depth):
    global ans
    children = reversed(g[i]) if depth % 2 == 1 else g[i]   # 深さに応じて走査順反転
    
    for v in children:
        if vals[v] == '(':
            # 括弧のノードならさらに深く潜る
            dfs(v, depth + 1)
        else:
            # 葉（文字）なら深さに応じて出力
            char = vals[v]
            if depth % 2 == 1:
                ans.append(char.swapcase())
            else:
                ans.append(char)

dfs(0,0)
print("".join(ans))


"""
S = '((XYZ)n(X(y)Z))'
→
g = [[1], [2, 6, 7], [3, 4, 5], [], [], [], [], [8, 9, 11], [], [10], [], []]
vals = [None, '(', '(', 'X', 'Y', 'Z', 'n', '(', 'X', '(', 'y', 'Z']


S = '(1+2*(3+4))'
→
g = [[1], [2, 3, 4, 5, 6], [], [], [], [], [7, 8, 9], [], [], []]
vals = [None, '(', '1', '+', '2', '*', '(', '3', '+', '4']
"""