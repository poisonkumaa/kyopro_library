#thanks to Shirotsume


class lazy_segtree():
    def update(self,k):self.d[k]=self.op(self.d[2*k],self.d[2*k+1])
    def all_apply(self,k,f):
        self.d[k]=self.mapping(f,self.d[k])
        if (k<self.size):self.lz[k]=self.composition(f,self.lz[k])
    def push(self,k):
        self.all_apply(2*k,self.lz[k])
        self.all_apply(2*k+1,self.lz[k])
        self.lz[k]=self.identity
    def __init__(self,V,OP,E,MAPPING,COMPOSITION,ID):
        self.n=len(V)
        self.log=(self.n-1).bit_length()
        self.size=1<<self.log
        self.d=[E for i in range(2*self.size)]
        self.lz=[ID for i in range(self.size)]
        self.e=E
        self.op=OP
        self.mapping=MAPPING
        self.composition=COMPOSITION
        self.identity=ID
        for i in range(self.n):self.d[self.size+i]=V[i]
        for i in range(self.size-1,0,-1):self.update(i)
    def set(self,p,x):
        p+=self.size
        for i in range(self.log,0,-1):self.push(p>>i)
        self.d[p]=x
        for i in range(1,self.log+1):self.update(p>>i)
    def get(self,p):
        p+=self.size
        for i in range(self.log,0,-1):self.push(p>>i)
        return self.d[p]
    def prod(self,l,r):
        if l==r:return self.e
        l+=self.size
        r+=self.size
        for i in range(self.log,0,-1):
            if (((l>>i)<<i)!=l):self.push(l>>i)
            if (((r>>i)<<i)!=r):self.push(r>>i)
        sml,smr=self.e,self.e
        while(l<r):
            if l&1:
                sml=self.op(sml,self.d[l])
                l+=1
            if r&1:
                r-=1
                smr=self.op(self.d[r],smr)
            l>>=1
            r>>=1
        return self.op(sml,smr)
    def all_prod(self):return self.d[1]
    def apply_point(self,p,f):
        assert 0<=p and p<self.n
        p+=self.size
        for i in range(self.log,0,-1):self.push(p>>i)
        self.d[p]=self.mapping(f,self.d[p])
        for i in range(1,self.log+1):self.update(p>>i)
    def apply(self,l,r,f):
        if l==r:return
        l+=self.size
        r+=self.size
        for i in range(self.log,0,-1):
            if (((l>>i)<<i)!=l):self.push(l>>i)
            if (((r>>i)<<i)!=r):self.push((r-1)>>i)
        l2,r2=l,r
        while(l<r):
            if (l&1):
                self.all_apply(l,f)
                l+=1
            if (r&1):
                r-=1
                self.all_apply(r,f)
            l>>=1
            r>>=1
        l,r=l2,r2
        for i in range(1,self.log+1):
            if (((l>>i)<<i)!=l):self.update(l>>i)
            if (((r>>i)<<i)!=r):self.update((r-1)>>i)
    def max_right(self,l,g):
        if l==self.n:return self.n
        l+=self.size
        for i in range(self.log,0,-1):self.push(l>>i)
        sm=self.e
        while(1):
            while(l%2==0):l>>=1
            if not(g(self.op(sm,self.d[l]))):
                while(l<self.size):
                    self.push(l)
                    l=(2*l)
                    if (g(self.op(sm,self.d[l]))):
                        sm=self.op(sm,self.d[l])
                        l+=1
                return l-self.size
            sm=self.op(sm,self.d[l])
            l+=1
            if (l&-l)==l:break
        return self.n
    def min_left(self,r,g):
        if r==0:return 0
        r+=self.size
        for i in range(self.log,0,-1):self.push((r-1)>>i)
        sm=self.e
        while(1):
            r-=1
            while(r>1 and (r%2)):r>>=1
            if not(g(self.op(self.d[r],sm))):
                while(r<self.size):
                    self.push(r)
                    r=(2*r+1)
                    if g(self.op(self.d[r],sm)):
                        sm=self.op(self.d[r],sm)
                        r-=1
                return r+1-self.size
            sm=self.op(self.d[r],sm)
            if (r&-r)==r:break
        return 0
    

# default
V = [i for i in range(8)] # [0, 1, 2, 3, 4, 5, 6, 7]

# 各種操作を定義
OP = max
E = float('inf')

# 区間加算なので、MAPPINGは「元の値+加算値」
MAPPING = lambda f, x: x + f 
# 加算処理の合成は、加算値を足し合わせるだけ
COMPOSITION = lambda f, g: f + g

#もし区間更新なら
#MAPPING = lambda f, x: f
#COMPOSITION = lambda f, g: f

# 何もしない加算は 0
ID = 0

# 遅延セグメント木のインスタンスを作成
seg = lazy_segtree(V, OP, E, MAPPING, COMPOSITION, ID)

    

#以下の操作をlog(N)で行える
#apply(l,r,f): 区間[l,r)区間にfをMAPPING
#get(i): i番目の要素を取得
#set(i, x): i番目の要素をxに更新
#prod(l,r): 区間クエリ処理。区間[l,r)に対するOPの結果(区間和、区間最大小)を返す

#max_right(l,g),mim_left(r,g): セグ木上の二分探索、O((logN)**2) -> O(log(N))にできる
#max_right(l,g): 区間[l,r)の計算結果が条件gを満たすような最大のrを求める
#min_left(r,g):  区間[l,r)の計算結果が条件gを満たすような最小のlを求める
#例) seg.max_right(2, lambda a: a <= 10): l=2から始めて、要素の合計が10を超えない範囲での最も右側のrを返す


#Sample---------------------------------------------

#「区間加算」と「区間最小値」**を求める問題を考える

# 元の配列
V = [i for i in range(8)] # [0, 1, 2, 3, 4, 5, 6, 7]

# 各種操作を定義
OP = min
E = float('inf')
# 区間加算なので、MAPPINGは「元の値+加算値」
MAPPING = lambda f, x: x +  f 
# 加算処理の合成は、加算値を足し合わせるだけ
COMPOSITION = lambda f, g:  g + f
# 何もしない加算は 0
ID = 0

# 遅延セグメント木のインスタンスを作成
seg = lazy_segtree(V, OP, E, MAPPING, COMPOSITION, ID)

# 区間[2, 6)の最小値を取得
print(seg.prod(2, 6)) # min(V[2]..V[5]) -> 2

# 区間[3, 7)の各要素に 10 を加算
seg.apply(3, 7, 10)
# この時点で内部配列は [0, 1, 2, 13, 14, 15, 16, 7] となっているはず

# 再度、区間[2, 6)の最小値を取得
# 対象範囲は [V[2], V[3]+10, V[4]+10, V[5]+10] -> [2, 13, 14, 15]
print(seg.prod(2, 6)) # -> 2

# 区間[0, 8)の最小値を取得
print(seg.prod(0, 8)) # min(0, 1, 2, 13, 14, 15, 16, 7) -> 0

# 区間[3:]で最小値が10以上となる最大の右側
print(seg.max_right(3,lambda x:x >= 10))  # -> 7

