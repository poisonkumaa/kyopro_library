import bisect

def binary_search(A, x):
    idx = bisect.bisect_left(A, x)
    return idx < len(A) and A[idx] == x

# 使用例
"""
A = [1, 3, 5, 7, 9, 11, 13]

print(binary_search(A, 5))  # True
print(binary_search(A, 6))  # False"
"""
