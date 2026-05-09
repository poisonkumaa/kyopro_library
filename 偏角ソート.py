# 偏角ソートは以下の関数を用いて、時計(反時計)周り、(a, b)を始点とするソートに変化可能、
# (a, b)を始点としたい場合はpointsに(a, b)をあらかじめ入れておく



from functools import cmp_to_key

def angular_sort_clockwise(points):
    """
    座標のリストを (0, 1) を始点として時計回りにソートして返す関数
    (0, 0) は (1, 0) と同じ偏角として扱う。
    
    Args:
        points (list[tuple[int, int]]): ソートしたい座標 (x, y) のリスト
    
    Returns:
        list[tuple[int, int]]: ソート済みのリスト
    """
    
    # 比較関数: 時計回り (Clockwise)
    def cmp(a, b):
        # (0, 0) は (1, 0) とみなして比較を行う
        ax, ay = a if a != (0, 0) else (1, 0)
        bx, by = b if b != (0, 0) else (1, 0)
        
        # 外積: z = ax * by - ay * bx
        z = ax * by - ay * bx
        
        if z == 0:
            return 0
        return -1 if z < 0 else 1

    # 領域を2つに分割
    # group1: (0, 1) から時計回りで (0, -1) の手前まで
    # group2: (0, -1) から時計回りで (0, 1) の手前まで
    group1 = []
    group2 = []
    
    for p in points:
        x, y = p
        
        # 領域判定
        # (1, 0) は x > 0 なので group1 に入る。
        # (0, 0) も group1 に入れたいため、条件に (x==0 and y==0) を追加
        if x > 0 or (x == 0 and y >= 0):
            group1.append(p)
        else:
            group2.append(p)
    
    # 各グループ内でソート
    group1.sort(key=cmp_to_key(cmp))
    group2.sort(key=cmp_to_key(cmp))
    
    return group1 + group2



# --- 以下、使用例 ---
if __name__ == "__main__":
    coords = [
        (1, 0),   # 3時
        (0, 1),   # 12時 (始点)
        (0, 0),   # 原点 (1, 0)と同じ扱いになる
        (-1, 0),  # 9時
        (0, -1),  # 6時
        (2, 0)    # (1, 0)と同じ方向
    ]

    sorted_coords = angular_sort_clockwise(coords)
    
    print("Sorted Result (Start from (0, 1), Clockwise):")
    # 予想される順序: (0, 1), (1, 0), (0, 0), (2, 0),... 同一直線上の順序は不定
    for p in sorted_coords:
        print(p)