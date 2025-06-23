def R(x,i):
    return (x+5*10**i)//10**(i+1)*10**(i+1)

# R(2100,2)  ---> 2000
# R(1234,0)  ---> 1230
x,i=map(int,input().split())
print(R(x,i))