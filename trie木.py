#ABC403-Eでの例を示す。
#ABC403

class Trie:
    class Node:
        __slots__ = ("child", "f", "Z")
        def __init__(self):
            self.child = {}    # char -> node index
            self.f = False     # is X 終端
            self.Z = set()     # このノード以下にある Y のクエリ番号

    def __init__(self):
        self.nodes = [self.Node()]
        self.Z = set()  # invalid Y のクエリ番号全体

    def add(self, s: str, idx: int, is_Y: bool):
        k = 0
        # 経路ノードを辿り／作りつつ、Y 挿入時は経路上の Z に idx を登録
        for c in s:
            node = self.nodes[k]
            if c not in node.child:
                node.child[c] = len(self.nodes)
                self.nodes.append(self.Node())
            if is_Y:
                node.Z.add(idx)
                if node.f:
                    # forbidden ノードを通った → invalid Y
                    self.Z.add(idx)
            k = node.child[c]

        node = self.nodes[k]
        if is_Y:
            # 終端ノードでも同様に
            node.Z.add(idx)
            if node.f:
                self.Z.add(idx)
        else:
            # X 挿入：このノードを forbidden にし、
            # これ以下にあるすべての Y を invalid に移す
            node.f = True
            self.Z |= node.Z
            node.Z.clear()


def main():
    Q = int(input())
    trie = Trie()
    total_Y = 0

    for qi in range(Q):
        t, s = input().split()
        if t == "1":
            # X 挿入
            trie.add(s, qi, is_Y=False)
        else:
            # Y 挿入
            total_Y += 1
            trie.add(s, qi, is_Y=True)

        # 有効な Y の数 = total_Y - invalid_Y の数
        print(total_Y - len(trie.Z))


if __name__ == "__main__":
    main()
