#ランレングス圧縮

def runlength_encode(S: str):
    if not S:
        return []
    rtn = []
    corrent_alphabet = S[0]
    start, end = 0, 0
    while start < len(S):
        while end < len(S) and S[end] == corrent_alphabet:
            end += 1
        rtn.append((corrent_alphabet, end - start))
        start = end
        if start >= len(S):
            break
        corrent_alphabet = S[start]
    return rtn


"""
S = ["A", "A", "A", "B", "B", "C"] 
print(runlength_encode(S))    #rtn == [("A", 3), ("B", 2), ("C", 1)]
"""


