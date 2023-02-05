import time 
import pandas as pd
import random

#variable of the problem 
n = 0
t0 = 0
customer = [0] #allowed delivered time of each customer
d = [0]   #the duration of unloading process of each customer's good
t = [] #traveling time matrix representation
c = [] #distance matrix representation

def input(test_case_dir):
    global n,t0,t,c,customer,d
    input_file = f'{test_case_dir}/input.txt'
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

def randomSolution():
    solution = [i for i in range(1,n+1)] 
    random.shuffle(solution)
    return [0] + solution 

def getRoutelength(solution):
    total_route = 0 
    for i in range(1,n+1):
        total_route += c[solution[i-1]][solution[i]]
    return total_route

def getNeighbors(solution):
    '''
        Get all the posible neighbors by swapping 2 i,j for all i != j and 1 <= i,j <= n
    '''
    neighbors = [] #store the neighbor
    for i in range(1,n):
        for j in range(i+1,n+1):
            neighbor = solution.copy()
            neighbor[i] = solution[j]
            neighbor[j] = solution[i]
            neighbors.append(neighbor)
    return neighbors

def check_TWC(res):   #check time window constraint
    time_current = t0
    for i in range(1, n+1):
        if time_current + t[res[i-1]][res[i]] + d[res[i]] <= customer[res[i]][1]:
            '''If the time at which the delivery man is ready to unload the good isn't reach the earliest
               time of customer res[k], then he need to wait until time customer[res[k]][0]'''
            if time_current + t[res[i-1]][res[i]] < customer[res[i]][0]:
                time_current = customer[res[i]][0] + d[res[i]]  #need to wait
            else:
                time_current += d[res[i]] + t[res[i-1]][res[i]]
        else:
            return False
    return True

def getBestNeighbor(neighbors):
    min_route = 1e10
    best_neighbor = []
    for neighbor in neighbors:
        if check_TWC(neighbor) == False:
            continue
        cur_route = getRoutelength(neighbor)
        if cur_route < min_route:
            min_route = cur_route
            best_neighbor = neighbor
    
    return best_neighbor, min_route

def Hill_Climbing():
    # Calculating the initial solution
    current_sol = randomSolution()  
    current_route_length = getRoutelength(current_sol)
    neighbors = getNeighbors(current_sol)
    best_neighbor , best_neighbor_route_length = getBestNeighbor(neighbors) 
    '''
        Calculate the neighbor whose route_length is minimum - the best_neighbor
        that we can find
    '''
    #Loop until stucking at local optimal solution
    while best_neighbor_route_length < current_route_length: 
        current_sol = best_neighbor
        current_route_length = best_neighbor_route_length
        neighbors = getNeighbors(current_sol)
        best_neighbor, best_neighbor_route_length = getBestNeighbor(neighbors)
    
    return current_sol, current_route_length

def run_test(test_case_dir):
    global n,t0,t,c,customer,d

    start_time = time.time()

    #variable initialize
    n = 0
    t0 = 0
    customer = [0] #allowed delivered time of each customer
    d = [0]   #the duration of unloading process of each customer's good
    t = [] #traveling time matrix representation
    c = [] #distance matrix representation
    input(test_case_dir)
    current_sol, current_route_length = Hill_Climbing()
    end_time = time.time()

    if check_TWC(current_sol) == False:
        return 'No feasible solution', end_time - start_time, n , 'No route'
    else:
        return current_route_length, end_time - start_time, n , current_sol[1:]

if __name__ == '__main__':
    results = [] # data to be exported to csv file 
    tmp = [3]  # test-th that you want to run 
    for i in range(10):
        test_case_dir = f'test_cases/test_{i}'
        print(f'Test case {i} is running ...')
        output, running_time, input_size , optimal_route = run_test(test_case_dir)
        with open(f'{test_case_dir}/output.txt','w') as f:
            f.write(str(output))
        print(f'Test case {i} finished in {running_time:.2f} second')
        results.append([i,input_size,output, running_time,str(optimal_route)])
    print('DONE')
    #Export data to csv file for analysis
    df = pd.DataFrame(results,  columns=['Test case','N = ?','Output','Running Time','Optimal Route'])
    df.to_csv('result_hill_climbing.csv', index = False)