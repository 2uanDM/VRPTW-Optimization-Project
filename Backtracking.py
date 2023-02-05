import time
import pandas as pd 

#variable for the problem
n = 0
t0 = 0
customer = [0] #allowed delivered time of each customer
d = [0]   #the duration of unloading process of each customer's good
t = [] #traveling time matrix representation
c = [] #distance matrix representation
#variable for implementing algorithm
res = []
mark = []
minn_distance = 1e10 
route = []

def input(test_case_dir):
    input_file = f'{test_case_dir}/input.txt'
    global n,t0,t,c,customer,d
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
        if time_current + t[res[i-1]][res[i]] + d[res[i]] <= customer[res[i]][1]:
            sum += c[res[i-1]][res[i]]
            '''If the time at which the delivery man is ready to unload the good isn't reach the earliest
               time of customer res[k], then he need to wait until time customer[res[k]][0]'''
            if time_current + t[res[i-1]][res[i]] < customer[res[i]][0]:
                time_current = customer[res[i]][0] + d[res[i]]  #need to wait
            else:
                time_current += d[res[i]] + t[res[i-1]][res[i]]
        else:
            return
    if minn_distance > sum:
        minn_distance = sum
        route.append([minn_distance, res[1:]])

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
    global res, mark, t, c, minn_distance,t0,route,customer,d
    start_time = time.time()
    t = []
    c = []
    route = []
    customer = [0]
    d = [0]
    input(test_case_dir)
    res = [0 for i in range(n+1)]
    mark = [0 for i in range(n+1)]
    minn_distance = 1e10
    Try(1)
    end_time = time.time()
    if minn_distance == 1e10:
        return 'No feasible solution', end_time - start_time, n , 'No route'
    else:
        return minn_distance, end_time - start_time, n , route[-1][1]

results = [] #data to be exported to csv

tmp = [2,3] #Since Backtracking costs so much time to run test with big N, so you can choose test to run
for i in range(20):
    test_case_dir = f'test_cases/test_{i}'
    print(f'Test case {i} is running ...')
    output, running_time, input_size , optimal_route = run_test(test_case_dir)
    with open(f'{test_case_dir}/output.txt', 'w') as f:
        f.write(str(output))
    print(f'Test case {i} finished in {running_time:.2f} second')
    results.append([i,input_size,output, running_time,str(optimal_route)])
print('DONE')
df = pd.DataFrame(results, columns=['Test case','N = ?','Output','Running Time','Optimal Route'])
df.to_csv('result_backtracking.csv',index= False)
