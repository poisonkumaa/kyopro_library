# 幾何ライブラリ
import math, sys
from typing import List, Tuple

# 注意点：直線と線分の区別、abs(p1 - p2)の誤差、

# ==============================================================================
# Constants & Basic Types
# ==============================================================================
# Point（点）はPythonの組み込み複素数型 `complex` を使用する。
# a + bi を x + yi とみなし、p.real で x 座標、p.imag で y 座標にアクセスする。
Point = complex
Polygon = List[Point]

EPS = 1e-8
PI = math.pi

# ==============================================================================
# Basic Utilities
# ==============================================================================
def eq(a: float, b: float) -> bool:
    """2つの実数 a, b が等しいかどうかを EPS の精度で判定する"""
    return abs(a - b) < EPS

def rotate(theta: float, p: Point) -> Point:
    """点 p を原点を中心に反時計回りに theta (ラジアン) 回転させる"""
    return p * complex(math.cos(theta), math.sin(theta))

def radian_to_degree(r: float) -> float:
    """ラジアンを度数法に変換する"""
    return r * 180.0 / PI

def degree_to_radian(d: float) -> float:
    """度数法をラジアンに変換する"""
    return d * PI / 180.0

def get_angle(a: Point, b: Point, c: Point) -> float:
    """線分 ab と線分 bc のなす角のうち、小さい方(0〜π)を返す"""
    v = b - a
    w = c - b
    alpha = math.atan2(v.imag, v.real)
    beta = math.atan2(w.imag, w.real)
    if alpha > beta:
        alpha, beta = beta, alpha
    theta = beta - alpha
    return min(theta, 2 * math.pi - theta)

# ==============================================================================
# Classes (直線と線分の使い分けに注意！！！！)
# ==============================================================================
class Line:
    """直線を表現するクラス"""
    def __init__(self, a: Point = 0j, b: Point = 0j, A: float = None, B: float = None, C: float = None):
        if A is not None and B is not None and C is not None:
            # Ax + By = C の一般形から直線を生成
            if eq(A, 0): self.a, self.b = complex(0, C / B), complex(1, C / B)
            elif eq(B, 0): self.a, self.b = complex(C / A, 0), complex(C / A, 1)
            else: self.a, self.b = complex(0, C / B), complex(C / A, 0)
        else:
            # 2点 a, b を通る直線を生成
            self.a = a
            self.b = b

class Segment(Line):
    """線分を表現するクラス (Lineを継承するが、交差判定などで区別して使用する)"""
    pass

class Circle:
    """円を表現するクラス"""
    def __init__(self, p: Point = 0j, r: float = 0.0):
        self.p = p  # 中心点
        self.r = r  # 半径

# ==============================================================================
# Vector Operations
# ==============================================================================
def cross(a: Point, b: Point) -> float:
    """2つのベクトル a, b の外積 (クロス積) を計算する。面積や回転方向の判定に使う"""
    return a.real * b.imag - a.imag * b.real

def dot(a: Point, b: Point) -> float:
    """2つのベクトル a, b の内積 (ドット積) を計算する。直交判定や射影に使う"""
    return a.real * b.real + a.imag * b.imag

# ==============================================================================
# Position / CCW (Counter-Clockwise)
# ==============================================================================
def ccw(a: Point, b: Point, c: Point) -> int:
    """
    点 a, b, c の位置関係を判定する (進行方向の判定)
    1: a -> b -> c が反時計回り (COUNTER_CLOCKWISE)
   -1: a -> b -> c が時計回り (CLOCKWISE)
    2: c -> a -> b の順で一直線上 (ONLINE_BACK)
   -2: a -> b -> c の順で一直線上 (ONLINE_FRONT)
    0: a -> c -> b の順で一直線上、または c が線分 ab 上 (ON_SEGMENT)
    """
    b -= a
    c -= a
    if cross(b, c) > EPS: return 1
    if cross(b, c) < -EPS: return -1
    if dot(b, c) < 0: return 2
    if abs(b) < abs(c): return -2
    return 0

def parallel(a: Line, b: Line) -> bool:
    """2つの直線 a, b が平行かどうかを判定する (外積が0なら平行)"""
    return eq(cross(a.b - a.a, b.b - b.a), 0.0)

def orthogonal(a: Line, b: Line) -> bool:
    """2つの直線 a, b が直交しているかを判定する (内積が0なら直交)"""
    return eq(dot(a.a - a.b, b.a - b.b), 0.0)

# ==============================================================================
# Projection / Reflection
# ==============================================================================
def projection(l: Line, p: Point) -> Point:
    """点 p から直線 l に下ろした垂線の足 (射影) を求める"""
    t = dot(p - l.a, l.a - l.b) / (abs(l.a - l.b) ** 2)
    return l.a + (l.a - l.b) * t

def reflection(l: Line, p: Point) -> Point:
    """直線 l を対称軸として、点 p と線対称にある点を求める"""
    return p + (projection(l, p) - p) * 2.0

# ==============================================================================
# Intersection (交差判定)
# ==============================================================================
def intersect_lp(l: Line, p: Point) -> bool:
    """直線 l と点 p が交差する (点 p が直線 l 上にある) かどうか判定"""
    return abs(ccw(l.a, l.b, p)) != 1

def intersect_ll(l: Line, m: Line) -> bool:
    """直線 l と直線 m が交差するかどうか判定 (平行でなければ交差する)"""
    return abs(cross(l.b - l.a, m.b - m.a)) > EPS or abs(cross(l.b - l.a, m.b - l.a)) < EPS

def intersect_sp(s: Segment, p: Point) -> bool:
    """線分 s と点 p が交差する (点 p が線分 s 上にある) かどうか判定"""
    return ccw(s.a, s.b, p) == 0

def intersect_ls(l: Line, s: Segment) -> bool:
    """直線 l と線分 s が交差するかどうか判定"""
    return cross(l.b - l.a, s.a - l.a) * cross(l.b - l.a, s.b - l.a) < EPS

def intersect_cl(c: Circle, l: Line) -> bool:
    """円 c と直線 l が交差するかどうか判定"""
    return distance_lp(l, c.p) <= c.r + EPS

def intersect_cp(c: Circle, p: Point) -> bool:
    """円 c の境界上に点 p があるかどうか判定"""
    return abs(abs(p - c.p) - c.r) < EPS

def intersect_ss(s: Segment, t: Segment) -> bool:
    """線分 s と線分 t が交差するかどうか判定"""
    return ccw(s.a, s.b, t.a) * ccw(s.a, s.b, t.b) <= 0 and ccw(t.a, t.b, s.a) * ccw(t.a, t.b, s.b) <= 0

def intersect_cs(c: Circle, l: Segment) -> int:
    """
    円 c と線分 l の交差判定
    戻り値: 0=交差しない, 1=1点で交差(接する、または片方の端点が円内), 2=2点で交差
    """
    h = projection(l, c.p)
    if abs(h - c.p) ** 2 - c.r * c.r > EPS: return 0
    d1 = abs(c.p - l.a)
    d2 = abs(c.p - l.b)
    if d1 < c.r + EPS and d2 < c.r + EPS: return 0
    if (d1 < c.r - EPS and d2 > c.r + EPS) or (d1 > c.r + EPS and d2 < c.r - EPS): return 1
    if dot(l.a - h, l.b - h) < 0: return 2
    return 0

def intersect_cc(c1: Circle, c2: Circle) -> int:
    """
    2つの円 c1, c2 の交差・包含関係 (共通接線の数) を判定する
    4: 離れている, 3: 外接する, 2: 交わる, 1: 内接する, 0: 内包する
    """
    if c1.r < c2.r: c1, c2 = c2, c1
    d = abs(c1.p - c2.p)
    if c1.r + c2.r < d: return 4
    if eq(c1.r + c2.r, d): return 3
    if c1.r - c2.r < d: return 2
    if eq(c1.r - c2.r, d): return 1
    return 0

# ==============================================================================
# Distance (距離)
# ==============================================================================
def distance_pp(a: Point, b: Point) -> float:
    """点 a と点 b の距離"""
    return abs(a - b)

def distance_lp(l: Line, p: Point) -> float:
    """直線 l と点 p の距離"""
    return abs(p - projection(l, p))

def distance_ll(l: Line, m: Line) -> float:
    """直線 l と直線 m の距離 (交差していれば0)"""
    return 0.0 if intersect_ll(l, m) else distance_lp(l, m.a)

def distance_sp(s: Segment, p: Point) -> float:
    """線分 s と点 p の距離"""
    r = projection(s, p)
    if intersect_sp(s, r): return abs(r - p)
    return min(abs(s.a - p), abs(s.b - p))

def distance_ss(a: Segment, b: Segment) -> float:
    """線分 a と線分 b の距離"""
    if intersect_ss(a, b): return 0.0
    return min(distance_sp(a, b.a), distance_sp(a, b.b),
               distance_sp(b, a.a), distance_sp(b, a.b))

def distance_ls(l: Line, s: Segment) -> float:
    """直線 l と線分 s の距離"""
    if intersect_ls(l, s): return 0.0
    return min(distance_lp(l, s.a), distance_lp(l, s.b))

# ==============================================================================
# Crosspoint (交点)
# ==============================================================================
def crosspoint_ll(l: Line, m: Line) -> Point:
    """直線 l と直線 m の交点を求める (平行でないことが前提)"""
    A = cross(l.b - l.a, m.b - m.a)
    B = cross(l.b - l.a, l.b - m.a)
    if eq(abs(A), 0.0) and eq(abs(B), 0.0): return m.a
    return m.a + (m.b - m.a) * B / A

def crosspoint_ss(l: Segment, m: Segment) -> Point:
    """線分 l と線分 m の交点を求める"""
    return crosspoint_ll(l, m)

def crosspoint_cl(c: Circle, l: Line) -> Tuple[Point, Point]:
    """円 c と直線 l の交点 (2点) を求める。接する場合は同じ点を2つ返す"""
    pr = projection(l, c.p)
    e = (l.b - l.a) / abs(l.b - l.a)
    if eq(distance_lp(l, c.p), c.r): return (pr, pr)
    base = math.sqrt(c.r * c.r - abs(pr - c.p) ** 2)
    return (pr - e * base, pr + e * base)

def crosspoint_cs(c: Circle, l: Segment) -> Tuple[Point, Point]:
    """円 c と線分 l の交点を求める"""
    aa = Line(l.a, l.b)
    if intersect_cs(c, l) == 2: return crosspoint_cl(c, aa)
    ret_first, ret_second = crosspoint_cl(c, aa)
    if dot(l.a - ret_first, l.b - ret_first) < 0:
        ret_second = ret_first
    else:
        ret_first = ret_second
    return (ret_first, ret_second)

def crosspoint_cc(c1: Circle, c2: Circle) -> Tuple[Point, Point]:
    """2つの円 c1, c2 の交点を求める"""
    d = abs(c1.p - c2.p)
    a = math.acos((c1.r * c1.r + d * d - c2.r * c2.r) / (2 * c1.r * d))
    t = math.atan2(c2.p.imag - c1.p.imag, c2.p.real - c1.p.real)
    p1 = c1.p + complex(math.cos(t + a) * c1.r, math.sin(t + a) * c1.r)
    p2 = c1.p + complex(math.cos(t - a) * c1.r, math.sin(t - a) * c1.r)
    return (p1, p2)

# ==============================================================================
# Tangent (接線)
# ==============================================================================
def tangent_cp(c: Circle, p: Point) -> Tuple[Point, Point]:
    """点 p を通る円 c の接線の接点を求める (2点)"""
    return crosspoint_cc(c, Circle(p, math.sqrt(abs(c.p - p)**2 - c.r**2)))

def tangent_cc(c1: Circle, c2: Circle) -> List[Line]:
    """2つの円 c1, c2 の共通接線を求める"""
    ret = []
    if c1.r < c2.r: c1, c2 = c2, c1
    g = abs(c1.p - c2.p) ** 2
    if eq(g, 0.0): return ret
    u = (c2.p - c1.p) / math.sqrt(g)
    v = rotate(PI * 0.5, u)
    for s in [-1, 1]:
        h = (c1.r + s * c2.r) / math.sqrt(g)
        if eq(1 - h * h, 0):
            ret.append(Line(c1.p + u * c1.r, c1.p + (u + v) * c1.r))
        elif 1 - h * h > 0:
            uu = u * h
            vv = v * math.sqrt(1 - h * h)
            ret.append(Line(c1.p + (uu + vv) * c1.r, c2.p - (uu + vv) * c2.r * s))
            ret.append(Line(c1.p + (uu - vv) * c1.r, c2.p - (uu - vv) * c2.r * s))
    return ret

# ==============================================================================
# Circumcenter & Minimum Enclosing Circle (外心・最小包含円)
# ==============================================================================
def circumcenter(a: Point, b: Point, c: Point) -> Point:
    """3点 a, b, c を通る円の中心（外心）を求める"""
    ab_mid = (a + b) / 2.0
    bc_mid = (b + c) / 2.0
    
    # 複素数に 1j を掛けると反時計回りに90度回転する性質を利用し、法線ベクトルを求める
    ab_dir = (a - b) * 1j
    bc_dir = (b - c) * 1j
    
    ab_line = Line(ab_mid, ab_mid + ab_dir)
    bc_line = Line(bc_mid, bc_mid + bc_dir)
    
    return crosspoint_ll(ab_line, bc_line)

def min_enclosing_circle_naive(p: List[Point]) -> Tuple[Point, float]:
    """
    点集合 p をすべて包含する最小の円の (中心座標, 半径) を求める。
    計算量 O(N^4)。N<=50 程度の制約向け。(ABC151-F Enclose All)
    """
    n = len(p)
    if n == 0: return (0j, 0.0)
    if n == 1: return (p[0], 0.0)
    
    alt: List[Point] = []
    
    # 中心候補の列挙
    for i in range(n):
        for j in range(i + 1, n):
            # 候補1: 2点を直径とする円の中心
            alt.append((p[i] + p[j]) / 2.0)
            
            for k in range(j + 1, n):
                # 3点が同一直線上にある場合はスキップ
                if abs(cross(p[j] - p[i], p[k] - p[i])) < EPS:
                    continue
                # 候補2: 3点を通る円の中心（外心）
                alt.append(circumcenter(p[i], p[j], p[k]))
                
    res_r = float('inf')
    res_c = 0j
    
    # 候補の中から最小の包含円を全探索
    for center in alt:
        tmp_r = 0.0
        for pt in p:
            tmp_r = max(tmp_r, abs(pt - center))
            
        if tmp_r < res_r:
            res_r = tmp_r
            res_c = center
            
    return res_c, res_r

# ==============================================================================
# Polygon (多角形)
# ==============================================================================
def is_convex(p: Polygon) -> bool:
    """多角形 p が凸多角形かどうか判定する。頂点は反時計回りに与えられる前提"""
    n = len(p)
    for i in range(n):
        if ccw(p[(i + n - 1) % n], p[i], p[(i + 1) % n]) == -1:
            return False
    return True

def convex_hull(p: Polygon) -> Polygon:
    """点集合 p の凸包 (すべての点を包含する最小の凸多角形) を求める。Monotone Chain Algorithm (O(N log N))"""
    """渡す点集合の順序は問わない。 返す点集合は凸包の反時計回りに並んだ状態のため、隣接点を結ぶ線が凸包を形成する"""
    n = len(p)
    if n <= 2: return p[:]
    # 辞書式順序でソート
    p = sorted(p, key=lambda z: (z.real, z.imag))
    ch = [0j] * (2 * n)
    k = 0
    # 下側凸包
    for i in range(n):
        while k >= 2 and cross(ch[k - 1] - ch[k - 2], p[i] - ch[k - 1]) < EPS:
            k -= 1
        ch[k] = p[i]
        k += 1
    t = k + 1
    # 上側凸包
    for i in range(n - 2, -1, -1):
        while k >= t and cross(ch[k - 1] - ch[k - 2], p[i] - ch[k - 1]) < EPS:
            k -= 1
        ch[k] = p[i]
        k += 1
    return ch[:k - 1]

def contains(Q: Polygon, p: Point) -> int:
    """
    多角形 Q と点 p の包含判定 (Winding Number Algorithm)
    戻り値: 0=OUT (外側), 1=ON (境界上), 2=IN (内側)
    """
    in_poly = False
    for i in range(len(Q)):
        a = Q[i] - p
        b = Q[(i + 1) % len(Q)] - p
        if a.imag > b.imag: a, b = b, a
        if a.imag <= 0 < b.imag and cross(a, b) < 0:
            in_poly = not in_poly
        if cross(a, b) == 0 and dot(a, b) <= 0:
            return 1 # ON
    return 2 if in_poly else 0

def convex_cut(U: Polygon, l: Line) -> Polygon:
    """凸多角形 U を直線 l (l.a -> l.b の向き) で切断し、その左側にできる凸多角形を返す"""
    ret = []
    for i in range(len(U)):
        now = U[i]
        nxt = U[(i + 1) % len(U)]
        if ccw(l.a, l.b, now) != -1:
            ret.append(now)
        if ccw(l.a, l.b, now) * ccw(l.a, l.b, nxt) < 0:
            ret.append(crosspoint_ll(Line(now, nxt), l))
    return ret

def area_polygon(p: Polygon) -> float:
    """多角形 p の面積を求める (外積の総和の半分)"""
    A = 0.0
    for i in range(len(p)):
        A += cross(p[i], p[(i + 1) % len(p)])
    return A * 0.5

def area_polygon_circle(p: Polygon, c: Circle) -> float:
    """円 c と多角形 p の共通部分の面積を求める"""
    if len(p) < 3: return 0.0
    
    def cross_area(c: Circle, a: Point, b: Point) -> float:
        va, vb = c.p - a, c.p - b
        f = cross(va, vb)
        ret = 0.0
        if eq(f, 0.0): return ret
        if max(abs(va), abs(vb)) < c.r + EPS: return f
        if distance_sp(Segment(a, b), c.p) > c.r - EPS:
            angle = math.atan2((vb / va).imag, (vb / va).real)
            return c.r * c.r * angle
        u = crosspoint_cs(c, Segment(a, b))
        tot = [a, u[0], u[1], b]
        for i in range(len(tot) - 1):
            ret += cross_area(c, tot[i], tot[i + 1])
        return ret

    A = 0.0
    for i in range(len(p)):
        A += cross_area(c, p[i], p[(i + 1) % len(p)])
    return A

def convex_diameter(p: Polygon) -> float:
    """凸多角形 p の直径 (最遠頂点対間の距離) をキャリパー法 (O(N)) で求める"""
    n = len(p)
    if n <= 1: return 0.0
    if n == 2: return abs(p[0] - p[1])
    is_, js_ = 0, 0
    # y座標が最小、最大の頂点を探す
    for i in range(1, n):
        if p[i].imag > p[is_].imag: is_ = i
        if p[i].imag < p[js_].imag: js_ = i
    
    maxdis = abs(p[is_] - p[js_]) ** 2
    i, maxi = is_, is_
    j, maxj = js_, js_
    
    # キャリパー法による探索
    while True:
        if cross(p[(i + 1) % n] - p[i], p[(j + 1) % n] - p[j]) >= 0:
            j = (j + 1) % n
        else:
            i = (i + 1) % n
        
        current_dis = abs(p[i] - p[j]) ** 2
        if current_dis > maxdis:
            maxdis = current_dis
            maxi, maxj = i, j
            
        # 一周したら終了
        if i == is_ and j == js_:
            break
            
    return math.sqrt(maxdis)

def closest_pair(ps: List[Point]) -> float:
    """平面走査 (分割統治法ベース) による最近点対の距離の計算 (O(N log N))"""
    if len(ps) <= 1: return 0.0
    ps = sorted(ps, key=lambda z: (z.real, z.imag))
    beet = [0j] * len(ps)
    INF = 1e18

    def rec(left: int, right: int) -> float:
        if right - left <= 1: return INF
        mid = (left + right) // 2
        x = ps[mid].real
        # 左右で再帰的に最小距離を求める
        ret = min(rec(left, mid), rec(mid, right))
        
        # Python組み込みのTimsortを利用し、y座標でマージ (in-place mergeの代用)
        ps[left:right] = sorted(ps[left:right], key=lambda z: z.imag)
        
        ptr = 0
        # 境界付近の点を走査して最小距離を更新
        for i in range(left, right):
            if abs(ps[i].real - x) >= ret: continue
            for j in range(ptr):
                luz = ps[i] - beet[ptr - j - 1]
                if luz.imag >= ret: break
                ret = min(ret, abs(luz))
            beet[ptr] = ps[i]
            ptr += 1
        return ret

    return rec(0, len(ps))





def how_to_use_1():  #1. 点・ベクトルと基本演算についての使用例
    # 点の定義 (実部がx座標、虚部がy座標)
    p1 = 3 + 4j
    p2 = 0 + 0j

    # 距離
    print(distance_pp(p1, p2))  # 5.0

    # 足し算、引き算 (ベクトル演算)
    v = p1 - p2
    print(v)  # (3+4j)

    # 点を原点中心に反時計回りに90度(π/2)回転
    p_rot = rotate(math.pi / 2, p1)
    print(p_rot)  # (-4.000000000000001+3.0000000000000004j)

    # 内積と外積
    a = 2 + 0j
    b = 0 + 2j
    print(dot(a, b))    # 0.0 (直交しているので内積は0)
    print(cross(a, b))  # 4.0 (外積は平行四辺形の面積)


def hot_to_use_2(): # 直線・線分と交差判定・交点についての使用例
    # 線分の定義
    s1 = Segment(0 + 0j, 5 + 5j)  # 原点から(5,5)への線分
    s2 = Segment(0 + 5j, 5 + 0j)  # (0,5)から(5,0)への線分

    # 交差判定
    if intersect_ss(s1, s2):
        print("線分は交差しています")
        # 交点を求める
        cp = crosspoint_ss(s1, s2)
        print(f"交点: {cp.real}, {cp.imag}")  # 交点: 2.5, 2.5

    # 距離
    s3 = Segment(0 + 10j, 5 + 10j)
    print(distance_ss(s1, s3))  # 5.0 ( (5,5) と (5,10) の距離 )

    # 射影 (点から直線に下ろした垂線の足)
    line = Line(0 + 0j, 5 + 0j) # x軸
    p = 3 + 4j
    proj = projection(line, p)
    print(f"射影: {proj.real}, {proj.imag}")  # 射影: 3.0, 0.0


def how_to_use_3(): # 円と接線・交点についての使用例
    # 中心(0, 0), 半径5の円
    c1 = Circle(0 + 0j, 5.0)
    # 中心(8, 0), 半径3の円
    c2 = Circle(8 + 0j, 3.0)

    # 円と円の交差判定
    status = intersect_cc(c1, c2)
    print(status)  # 3 (外接する)

    if status <= 3:  # 交点を持つ場合 (内包/内接/交わる/外接)
        cp1, cp2 = crosspoint_cc(c1, c2)
        print(f"交点1: {cp1.real}, {cp1.imag}")
        print(f"交点2: {cp2.real}, {cp2.imag}")

    # 点から円への接線
    p_out = 10 + 0j
    tangents = tangent_cp(c1, p_out)
    print(f"接点1: {tangents[0]}")
    print(f"接点2: {tangents[1]}")


def how_to_use_4(): # 多角形 (凸包・面積・切断) についての使用例  
    # 多角形は点のリスト (List[complex]) として扱う。必ず「反時計回り」に頂点が並ぶように注意すること
    # 凸包に渡すときは自動ソートしてくれる

    points = [0+0j, 4+0j, 4+4j, 0+4j, 2+2j]

    # 1. 凸包を求める
    hull = convex_hull(points)
    print(f"凸包の頂点数: {len(hull)}")  # 4 (内側の2+2jが除かれる)
    for p in hull:
        print(f"({p.real}, {p.imag})") # (0,0)->(4,0)->(4,4)->(0,4)の順に出力

    # 2. 多角形の面積
    print(f"面積: {area_polygon(hull)}")  # 16.0

    # 3. 点の包含判定
    test_p1 = 2 + 2j # 内側
    test_p2 = 5 + 5j # 外側
    print(contains(hull, test_p1))  # 2 (IN)
    print(contains(hull, test_p2))  # 0 (OUT)

    # 4. 凸多角形の切断 (直線 y = x で切断し、左上側の多角形を取得)
    cut_line = Line(0 + 0j, 5 + 5j) 
    cut_poly = convex_cut(hull, cut_line)
    print(f"切断後の面積: {area_polygon(cut_poly)}")  # 8.0 (半分の三角形になる)




if __name__ == "__main__": 
    # 1点の読み込み
    x, y = map(float, input().split())
    p = complex(x, y)

    # N点の読み込み
    N = int(input())
    points = []
    for _ in range(N):
        x, y = map(float, input().split())
        points.append(complex(x, y))