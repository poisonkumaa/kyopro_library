#N*N行列Aに対してA**nを返す(modをとる)
#O(N*N*log_n)

def pow_mat(A: list, n: int, mod):
    # A**nを計算(各値modをとる)
    def matmul(A, B):
        #行列A * Bを計算
        N, M, L  = len(A), len(B[0]), len(B)
        c = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(M):
                for k in range(L):
                    c[i][j] += A[i][k] * B[k][j]
                    c[i][j] %= mod                           
        return c
    
    #Aのcheck
    N = len(A)
    for i in range(len(A)):
        if len(A[i]) != N:
            return -1
        
    y = [[0] * N for _ in range(N)]
    for i in range(N):
        y[i][i] = 1

    while n > 0:
        if n & 1:
            y = matmul(A, y)
        A = matmul(A, A)
        n >>= 1
    return y
    

"""
A = [[2,0],[0,2]]
mod = 998244353
print(pow_mat(A, 4, mod))
"""
    
    
