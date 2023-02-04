import time
import pandas as pd 

#variable for the problem
n = 0
t0 = 0
customer = [0] #allowed delivered time of each customer
d = [0]   #the duration of unloading process of each customer's good
t = []    #traveling time matrix representation
c = []    #distance matrix representation
res = []
mark = []
sum_distance = 0  #the sum of the distance the man have traveled at customer k
time_current = 0
minn_distance = 1e10 
c_min = 1e10      #the minimum distance between each pair of customers
route = [] 

def input(test_case_dir):
    input_file = f'{test_case_dir}/input.txt'
    global n,t0,c,t
    with open(input_file, 'r') as f:
        n = int(f.readline())
        t0 = int(f.readline())
        for i in range(n):
            u,v,w = map(int, f.readline().split())
            customer.append([u,v])
            d.append(w)
        for i in range(n+1):
            t.append(list(map(int, f.readline().split())))
        for i in range(n+1):
            c.append(list(map(int, f.readline().split())))

def solution():
    global minn_distance
    if sum_distance < minn_distance:
        minn_distance = sum_distance
        route.append([minn_distance, res[1:]])

def lower_bound(k):
    if minn_distance > sum_distance + (n-k) * c_min:
        return True
    return False

def upper_bound(k):
    if time_current <= customer[res[k]][1]:
        return True
    return False

def Try(k): #Branching process
    global sum_distance,time_current
    for i in range(1,n+1):
        if mark[i] == 0:
            res[k] = i
            mark[i] = 1
            sum_distance += c[res[k-1]][res[k]]
            '''If the time at which the delivery man is ready to unload the good isn't reach the earliest
               time of customer res[k], then he need to wait until time customer[res[k]][0]'''
            if time_current + t[res[k-1]][res[k]] < customer[res[k]][0]:
                need_wait = True
                tmp = time_current
                time_current = customer[res[k]][0] + d[res[k]]  #need to wait
            else:
                need_wait = False
                time_current += d[res[k]] + t[res[k-1]][res[k]]  #don't need to wait

            if k == n:
                solution() # Update min_distance 
            else:
                if lower_bound(k) == True and upper_bound(k) == True:
                    Try(k+1)
            #Restore the previous state 
            sum_distance -= c[res[k-1]][res[k]]
            if need_wait == True:
                time_current = tmp
            else:
                time_current -= d[res[k]] + t[res[k-1]][res[k]]
            mark[i] = 0
            res[k] = 0

def run_test(test_case_dir):
    global res, mark, t, c, minn_distance, sum_distance,c_min,time_current,t0, route
    start_time = time.time()
    t = []
    c = []
    route = []
    c_min = 1e10
    minn_distance = 1e10
    sum_distance = 0
    #get data of each test case
    input(test_case_dir)
    time_current = t0
    res = [0 for i in range(n+1)]
    mark = [0 for i in range(n+1)]
    #Finding the minimum distance > 0 between each pair of customers 
    not_zero_c = [i for x in c for i in x if i != 0]
    for x in not_zero_c:
        c_min = min(c_min,x)
    Try(1)
    end_time = time.time()
    if minn_distance == 1e10:
        return 'No feasible solution', end_time - start_time, n , 'No route'
    else:
        return minn_distance, end_time - start_time, n , route[-1][1]

results = [] #data to be exported to csv
num_tests = 100 
tmp = [1] #Since Backtracking costs so much time to run test with big N, so you can choose test to run
for i in range(9):
    test_case_dir = f'test_cases/test_{i}'
    print(f'Test case {i} is running ...')
    output, running_time, input_size, optimal_route = run_test(test_case_dir)
    with open(f'{test_case_dir}/output.txt', 'w') as f:
        f.write(str(output))
    print(f'Test case {i} finished in {running_time:.2f} second')
    results.append([i,input_size,output, running_time,str(optimal_route)])
print('DONE')
df = pd.DataFrame(results, columns=['Test case','N = ?','Output','Running Time','Optimal Route'])
df.to_csv('result_ver_fix.csv',index= False)