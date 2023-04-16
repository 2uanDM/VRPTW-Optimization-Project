import time
import pandas as pd

#variable for the problem
n = 0
t0 = 0
customer = [0] #allowed delivered time of each customer
d = [0]   #the duration of unloading process of each customer's good
t = []    #traveling time matrix representation
c = []    #distance matrix representation

def input(test_case_dir):
    input_file = f'{test_case_dir}/input.txt'
    global n,t0,customer,d,t,c
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

def check_TWC(time_current,res,k,val): #check the time window constraints
    if time_current + t[res[k-1]][val] + d[val] <= customer[val][1]:
        return True
    return False

def Greedy():
    res = [0 for i in range(n+1)]   #Store the solution
    mark = [False for i in range(n+1)] #Check whether element i exist in the solution or not
    time_current = t0
    min_distance = 0    

    for k in range(1,n+1): #Building the k - element
        feasible = []      #Store the values whose time window constraints are satisfied with the built solution
        for val in range(1,n+1):
            if mark[val] == False and check_TWC(time_current, res, k, val) == True:
                feasible.append([val, c[res[k-1]][val] ])
        
        if feasible == []: #After evaluating all the possible value, if there is no value is feasible -> return
            return -1, -1
        #else find the solution whose cost is the minimum 
        feasible.sort(key = lambda x: x[1])
        min_distance += feasible[0][1]
        res[k] = feasible[0][0]
        mark[feasible[0][0]] = True
        if time_current + t[res[k-1]][res[k]] < customer[res[k]][0]:
                time_current = customer[res[k]][0] + d[res[k]]  #need to wait
        else:
            time_current += d[res[k]] + t[res[k-1]][res[k]]
    
    return min_distance, res[1:]

def run_test(test_case_dir):
    global n,t0,t,c,customer,d
    start_time = time.time()
    #variable initialize
    n = 0
    t0 = 0
    customer = [0] #allowed delivered time of each customer
    d = [0]   #the duration of unloading process of each customer's good
    t = []    #traveling time matrix representation
    c = []    #distance matrix representation
    input(test_case_dir)
    min_distance, optimal_route = Greedy()
    end_time = time.time()

    if min_distance == -1:
        return 'No feasible solution', end_time - start_time, n , 'No route'
    else:
        return min_distance, end_time - start_time, n , optimal_route

if __name__ == '__main__':
    results = [] # data to be exported to csv file 
    tmp = [2]  # test-th that you want to run 
    for i in range(100):
        test_case_dir = f'test_cases/test_{i}'
        print(f'Test case {i} is running ...')
        output, running_time, input_size , optimal_route = run_test(test_case_dir)
        with open(f'{test_case_dir}/output.txt','w') as f:
            f.write(str(output))
        print(f'Test case {i} finished in {running_time:.2f} second')
        results.append([i,input_size,output, running_time,str(optimal_route)])
    print('DONE')
    #Export data to csv file for analysis
    df = pd.DataFrame(results,  columns=['Test case','N = ?','Output','Running Time','Nearly Optimal Route'])
    df.to_csv('result_greedy.csv', index = False)
