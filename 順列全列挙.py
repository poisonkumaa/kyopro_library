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
