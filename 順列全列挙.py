import itertools

#s = input()
s = "aab"
s1 = []
for i in itertools.permutations(s):    #nPr
    s_temp = "".join(i)
    s1.append(s_temp)
print(s1)

s2 = []
s2set = set()
for i in itertools.combinations(s,2):    #nCr
    s_temp = "".join(i)
    s2.append(s_temp)
    s2set.add(s_temp)
print(s2)
print(s2set)

s3 = []
for i in itertools.combinations_with_replacement(s,3):  #nHr
    s_temp  = "".join(i)
    s3.append(s_temp)
print(s3)


#pythonではmore_itertoolsのdistinct_permutationを用いることで重複なしの並び替えが高速に動作する(len(S) = 10 で700ms)
#参考：Avoid K Palindrome 2
from more_itertools import distinct_permutations
S = "abcdefghij"
ans = 0
for s in distinct_permutations(S):
    #print(s)
    ans += 1
print(ans)


