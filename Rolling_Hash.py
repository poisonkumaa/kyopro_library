#thanks to Shirotsume
#rh = Rollinghash(S,base,mod)としておくことで、Sの任意の範囲のハッシュ値をO(1)で取得できる
#生成：O(|S|)

import random
inf = 2 ** 61 - 1

mod = inf

base = random.randint(1, mod - 1)
class Rollinghash:
    def __init__(self, string, base, mod):
        n = len(string)
        self.__base = base
        self.__mod = mod
        self.__hash = [0]*(n + 1)
        self.__pow = [1]*(n + 1)
        if isinstance(string, str):
            for i, c in enumerate(string):
                o = ord(c) - ord('a') + 1
                self.__hash[i + 1] = (self.__hash[i] * self.__base + o) % self.__mod
                self.__pow[i + 1] = self.__pow[i] * self.__base % self.__mod
        else:
            for i, c in enumerate(string):
                o = c
                self.__hash[i + 1] = (self.__hash[i] * self.__base + o) % self.__mod
                self.__pow[i + 1] = self.__pow[i] * self.__base % self.__mod

   
    def query(self, l, r):
        ret = (self.__hash[r] - self.__hash[l] * self.__pow[r - l]) % self.__mod
        return ret
    def same(self, l1, r1, l2, r2):
        return self.query(l1, r1) == self.query(l2, r2)
    

#例    
S = "ABCDEABCDE"
rlh = Rollinghash(S,base,mod)
print(rlh.same(0,5,5,10))  #0～4文字目と5～9文字目の比較

l = 0; r = 2
print(rlh.query(l,r))    #[l,r)範囲をhash値に変換

