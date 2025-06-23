import sys
input = lambda: sys.stdin.readline().rstrip()
ii = lambda: int(input())
mi = lambda: map(int, input().split())
li = lambda: list(mi())
#https://procon.fun/code/spiral/
#by cd1024_div2

t = ii()
for _ in range(t):
    #中心部分からぐるぐる0 -> n**2-1まで
    n = ii()
    H =  n
    W   = n #列数
    myMap = [[-1] * W for h in range(H)]
    
    num = H * W #マスの総数
    h, w = 0, 0 #初期位置
    dh, dw = 0, 1 #移動するために加算する変数。詳細は後述。
    cnt = 0 #マスに書き込む数 および 探索数管理用
    while cnt < num:
        myMap[h][w] = n * n - 1 - cnt
        cnt += 1
    #    右端の列を超えた or 左端の列を超えた or 下端の行を超えた or 上端の行を超えた or すでに訪れたことのあるマスに到達した 
        if w + dw >= W or w + dw < 0 or h + dh >= H or h + dh < 0 or myMap[h+dh][w+dw] != -1:
        
            dh, dw = dw, -dh
        h += dh
        w += dw

    for m in myMap:
        print(*m) #--> [8, 7, 6]
             #    [1, 0, 5]
             #    [2, 3, 4]

