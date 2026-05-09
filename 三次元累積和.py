import sys
input = lambda: sys.stdin.readline().rstrip()
ii = lambda: int(input())
mi = lambda: map(int, input().split())
li = lambda: list(mi())

#ABC366-D Cuboid Sum Queryより
#三次元累積和
#pre[i][j][k]: (1, 1, 1) ~ (i, j, k)までの総和
#indexに注意

N = ii()
A = [[li() for _ in range(N)] for _ in range(N)]
Q = ii()
pre = [[[0] * (N+1) for _ in range(N+1)] for _ in range(N+1)]
for i in range(N):
    for j in range(N):
        for k in range(N):
            pre[i+1][j+1][k+1] = ( (pre[i][j+1][k+1] + pre[i+1][j][k+1] + pre[i+1][j+1][k]) 
                                - (pre[i+1][j][k] + pre[i][j+1][k] + pre[i][j][k+1])
                                + pre[i][j][k] + A[i][j][k]
            )
for _ in range(Q):
    lx, rx, ly, ry, lz, rz = mi()
    #lx-=1;rx-=1;ly-=1;ry-=1;lz-=1;rz-=1
    print(pre[rx][ry][rz] - pre[lx-1][ry][rz] - pre[rx][ly-1][rz] - pre[rx][ry][lz-1] + pre[rx][ly-1][lz-1] + pre[lx-1][ry][lz-1] + pre[lx-1][ly-1][rz] - pre[lx-1][ly-1][lz-1])


