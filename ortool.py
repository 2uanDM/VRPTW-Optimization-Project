from ortools.linear_solver import pywraplp
import pandas as pd
import time

def run_test(test_case_dir):   
    start_time = time.time()
    #Create the MIP solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    #Input data from file 
    input_file = f'{test_case_dir}/input.txt'
    f = open(input_file, 'r')

    #Initialize some variables:
    customer = [0]
    d = [0]
    t = []
    c = []

    #Input data of the variables:
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

    # Define the binary variables x[i][j] to represent visiting city i before j
    x = {}
    for i in range(n+1):
        for j in range(n+1):
            if i != j:
                x[i,j] = solver.BoolVar('x[%i, %i]' % (i,j))
    # Define the variable t_current
    t_current = [t0] + [solver.NumVar(0, solver.infinity(), 't_current_%i' % i)\
             for i in range(1,n+1)]
    for j in range(1,n+1):
        for i in range(n+1):
            if i != j:
                t_current[j] = t_current[i] + t[i][j] * x[i,j]

    # Define the constraint: Each customer is visited once:
    for j in range(1, n+1): #for all customer
        solver.Add(sum(x[i,j] for i in range(n+1) if i != j) == 1)
        solver.Add(sum(x[j,i] for i in range(1,n+1) if i!= j) == 1)

    #Define the constraint: Start at warehouse (point 0):
    solver.Add(sum(x[0,i] for i in range(1,n+1)) == 1)

    #Defined the time window constraint 1: 
    constraint_1 = lambda : all(customer[i][0] + d[i] <= customer[i][1] for i in range(1,n+1))
    solver.Add(constraint_1())

    #Defined the time window constraint 2:
    constraint_2 = lambda : all(t_current[i] + d[i] <= customer[i][1] for i in range(1,n+1))
    solver.Add(constraint_2())
    
    #Define the objective function
    solver.Minimize(sum(c[i][j] * x[i,j] for i in range(n+1) for j in range(1,n+1) if i!= j))

    #Call the solver
    status = solver.Solve()
    end_time = time.time()
    if status == pywraplp.Solver.OPTIMAL:
        return solver.Objective().Value(), end_time - start_time, n, status
    else:
         return 'No feasible solution', end_time - start_time, n , status

def main():
    results = [] # data to be exported to csv file 
    tmp = [2]  # test-th that you want to run 
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
    df = pd.DataFrame(results,  columns=['Test case','N = ?','Output','Running Time','Nearly Optimal Route'])
    df.to_csv('result_ortool.csv', index = False)

if __name__ == '__main__':
    main()