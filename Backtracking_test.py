import time
#variables defined 
customer = ['index 0']
d = ['index 0']
t = [] #traveling time matrix representation
c = [] #distance matrix representation

def input():
    input_file = 'input.txt'
    global n,t0
    with open(input_file, 'r') as f:
        n = int(f.readline())
        t0 = int(f.readline())
        for i in range(n):
            u,v,w= map(int, f.readline().split())
            customer.append([u,v])
            d.append(w)
        for i in range(n+1):
            t.append(list(map(int, f.readline().split())))
        for i in range(n+1):
            c.append(list(map(int, f.readline().split())))

input()

res = [0 for i in range(n+1)]    # Array to store the current solution
mark = [0 for i in range(n+1)]   # Whether customer i is visited or not 
minn_distance = 1e10 

def solution():
    global minn_distance
    time_current = t0
    sum = 0 # total distance moved
    for i in range(1, n+1):
        if time_current + t[res[i-1]][res[i]] <= customer[res[i]][1]:
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
start_time = time.time()
Try(1)
end_time = time.time()
output_file = 'output.txt'
with open(output_file, 'w') as f:
    if minn_distance == 1e10:
        f.write('No feasible solution' + '\n' + str(end_time - start_time))
    else:
        f.write(str(minn_distance) + '\n' + str(end_time - start_time))