import sys 
#variables defined 
customer = ['index 0']
d = ['index 0']
t = [] #traveling time matrix representation
c = [] #distance matrix representation

def input():
    global n,t0
    n = int(input())
    t0 = int(input())
    for i in range(n):
        u,v,w= list(map(int, input().split()))
        customer.append([u,v])
        d.append(w)
    for i in range(n+1):
        t.append(list(map(int, input().split())))
    for i in range(n+1):
        c.append(list(map(int, input().split())))

res = [0 for i in range(n+1)] 
mark = [0 for i in range(n+1)]
minn_distance = 1e10 

def solution():
    time_current = t0
    sum = 0 # total distance moved
    for i in range(1, n+1):
        if time_current + t[res[i-1]][res[i]] <= customer[res[i]][0]:
            sum += c[res[i-1]][res[i]]
            time_current += d[res[i]] + t[res[i-1]][res[i]]
        else:
            return
    minn_distance = min(minn_distance, sum)

def Try(k):
    for i in range(1,n+1):
        if mark[i] == 0:
            res[k] = i
            mark[i] = 1
            if k == n:
                solution()
            else:
                Try(k+1)
        mark[i] = 0

#main
input()
Try(1)
print(minn_distance)
