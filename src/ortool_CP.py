from ortools.sat.python import cp_model
import time
import pandas as pd

def run_test(test_case_dir):
    start_time = time.time()
    
    # Input data from input.txt
    input_file = f'{test_case_dir}/input.txt'
    f = open(input_file, 'r')
    N = int(f.readline())
    t0 = int(f.readline())
    e = [0]
    l = [0]
    d = [0]
    t = []
    c = []
    for i in range(1,N+1):
        u,v,w = map(int, f.readline().split())
        e.append(u)
        l.append(v)
        d.append(w)
    for i in range(N+1):
        t.append(list(map(int, f.readline().split())))
    for i in range(N+1):
        c.append(list(map(int, f.readline().split())))

    # Create a model
    model = cp_model.CpModel()

    # Define the variables
    x = {}      #binary variable x[i,j] = 1if customer j is visited after customer i
    s = {}      #
    for i in range(N+1):
        s[i] = model.NewIntVar(0, int(1e6), f's[{i}]')
        for j in range(N+1):
            if i != j:
                x[i, j] = model.NewBoolVar(f'x[{i},{j}]')
    # Time window constraint
    for i in range(1, N+1):
        model.Add(s[i] + d[i] <= l[i])
        model.Add(s[i] >= e[i])

    # Travel time constraint:
    for i in range(N+1):
        for j in range(N+1):
            if i != j:
                model.Add(s[i] + d[i] + t[i][j] <= s[j]).OnlyEnforceIf(x[i, j])
    
    # s[0] = the starting time t0
    model.Add(s[0] == t0)

    # Constraint: Must start from point 0
    model.Add(sum(x[0, j] for j in range(1, N+1)) == 1)
    
    #Constraint: Each customer is visited once
    for i in range(1,N+1):
        model.Add(sum(x[j,i] for j in range(0,N+1) if i!=j) == 1)
    for i in range (0,N+1):
        model.Add(sum(x[i,j] for j in range(1,N+1) if i!=j) <=1)
    
    #Constraint: For a pair of two customers, there is at most one way from this one to another one
    for i in range(N+1):
        for j in range(N+1):
            if i != j:
                model.Add(x[i, j] + x[j, i] <= 1)

    # Define the objective function
    obj = sum(c[i][j] * x[i, j] for i in range(N+1) for j in range(N+1) if i!=j)
    model.Minimize(obj)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    end_time = time.time()

    #If there is no optimal soluiton
    if status == 3:
        return 'No feasible solution', end_time - start_time, N , 'No route'
        
    # Get the optimal solution
    tmp = []
    for i in range(N+1):
        for j in range(1,N+1):
            if i!= j:
                if solver.Value(x[i,j]) == 1:
                    tmp.append([i,j])
    
    start = 0
    route = []
    while len(route) < N:
        for x in tmp:
            if x[0] == start:
                start = x[1]
                route.append(x[1])
                break

    return solver.Value(obj), end_time - start_time, N, route
  

if __name__ == '__main__':
    results = [] # data to be exported to csv file 
    tmp = [2]  # test-th that you want to run 
    for i in range(28):
        test_case_dir = f'test_cases/test_{i}'
        print(f'Test case {i} is running ...')
        output, running_time, input_size , optimal_route = run_test(test_case_dir)
        print(f'Test case {i} finished in {running_time:.2f} second')
        results.append([i,input_size,output, running_time,str(optimal_route)])
    print('DONE')
    #Export data to csv file for analysis
    df = pd.DataFrame(results,  columns=['Test case','N = ?','Output','Running Time','Nearly Optimal Route'])
    df.to_csv('result_CP.csv', index = False)

