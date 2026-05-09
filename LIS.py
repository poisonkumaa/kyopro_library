from bisect import bisect_left, bisect_right


# seqのLISの長さを返す. 具体的なLISを求めているわけではない
def make_lis(seq):
    LIS = [seq[0]]
    for i in range(len(seq)):
        if seq[i] > LIS[-1]:
            LIS.append(seq[i])
        else:
            LIS[bisect_left(LIS, seq[i])] = seq[i]

    print(len(LIS))


# rtn[i]: seq[i]を最後の要素とするLISの長さを返す. 具体的なLISを求めているわけではない
def make_part_lis(seq):
    rtn = []
    LIS = [seq[0]]
    for i in range(len(seq)):
        if seq[i] > LIS[-1]:
            LIS.append(seq[i])
        else:
            LIS[bisect_left(LIS, seq[i])] = seq[i]
        rtn.append(bisect_left(LIS, seq[i]) + 1)   # ここで二分探索することで"seq[i]を最後の要素とする"が達成できる
    return rtn




# 具体的なLISを求める方法(return_idx_flgをTrueにするとidxを返す)

def lis(arr: list[int], return_idx_flg: bool = False) -> list[int]: 
    n = len(arr)
    inf = 2 ** 61 - 1
    dp1 = [inf] * n
    dp2 = [-1] * n
    for i, a in enumerate(arr):
        idx = bisect_left(dp1, a)   # 広義単調増加ならbisect_rightにする
        dp1[idx] = a
        dp2[i] = idx
    idx = max(dp2)
    lis = [0] * (idx + 1)
    lis_idx = [0] * (idx + 1)
    for i, a in enumerate(arr[::-1]):
        if dp2[~i] == idx:
            lis[idx] = a
            lis_idx[idx] = n - i - 1
            idx -= 1
    if 1: #debug
        print("dp1:",dp1)
        print("dp2:",dp2)  # dp2[i] == j: arr[i]はLISのj番目になる可能性がある
        print("lis:",lis)
        print("lis_idx:", lis_idx)
        print("return_idx:", return_idx_flg)
    return lis_idx if return_idx_flg else lis



print(lis([3,4,8,5,5,6,2,7]))