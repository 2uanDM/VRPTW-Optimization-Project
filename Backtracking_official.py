import time
import pandas as pd 

#variable for the problem
n = t0 = 0
customer = [0] #allowed delivered time of each customer
d = [0]   #the time needed to deliver each good
t = [] #traveling time matrix representation
c = [] #distance matrix representation
res = []
mark = []
minn_distance = 1e10 


def input(test_case_dir):
    input_file = f'{test_case_dir}/input.txt'
    global n,t0,t,c
    with open(input_file, 'r') as f:
        n = int(f.readline())
        t0 = int(f.readline())
        for i in range(n):
            u,v,w =  map(int, f.readline().split())
            customer.append([u,v])
            d.append(w)
        for i in range(n+1):
            t.append(list(map(int, f.readline().split())))
        for i in range(n+1):
            c.append(list(map(int, f.readline().split())))   

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

def Try(k): #Backtracking
    for i in range(1,n+1):
        if mark[i] == 0:
            res[k] = i
            mark[i] = 1
            if k == n:
                solution()
            else:
                Try(k+1)
            mark[i] = 0

def run_test(test_case_dir):
    global res, mark, t, c, minn_distance
    start_time = time.time()
    t = []
    c = []
    input(test_case_dir)
    res = [0 for i in range(n+1)]
    mark = [0 for i in range(n+1)]
    minn_distance = 1e10
    Try(1)
    end_time = time.time()
    return minn_distance, end_time - start_time

results = [] #data to be exported to csv
num_tests = 100 
tmp = [1,2,3,4,5,6,7,8]
for i in tmp:
    test_case_dir = f'test_cases/test_{i}'
    output, running_time = run_test(test_case_dir)
    results.append([i,output, running_time])

df = pd.DataFrame(results, columns=['Test case','Output','Running Time'])
df.to_csv('result.csv',index= False)
