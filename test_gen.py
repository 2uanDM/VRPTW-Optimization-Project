import random
import os 

#Defined the number of customers and the number of tests:
test_th = 0
a = [10]

def tests(N) -> int:
    if N in [6,8]:
        return 30
    elif N in [10,12,14]:
        return 10
    else:
        return 4
        
for N in range(2,17,2):
    u = tests(N)
    for test_num in range(u):
        #Create a folder for each test case:
        test_dir = "test_" + str(test_th)
        test_th += 1
        os.mkdir(test_dir) #create a folder named test_dir

        #generate random t0
        t0 = random.randint(0,10)

        #generate random e,i,d for each customer 
        e = [random.randint(0,100) for i in range(N+1)]
        d = [random.randint(1,10) for i in range(N+1)]
        l = [random.randint(e[i] + d[i],200) for i in range(N+1)] #ensure that e[i] + d[i] <= l[i]
        

        #generate symmetric traveling time and distance matrices
        t = [[0] * (N+1) for _ in range(N+1)] 
        c = [[0] * (N+1) for _ in range(N+1)]
        for i in range(0,N+1):
            for j in range(0,N+1):
                if i != j:
                    t[i][j] = t[j][i] = random.randint(1,15)
                    c[i][j] = c[j][i] = random.randint(1,15)
        
        #write input file for the test case
        input_file = os.path.join(test_dir, 'input.txt')
        with open(input_file, 'w') as f:
            f.write(str(N) + '\n')

            f.write(str(t0) + '\n')
            
            for i in range(1,N+1):
                f.write(str(e[i]) + ' ' + str(l[i]) + ' ' + str(d[i]) + '\n')

            for i in range(0,N+1):
                for j in range(0,N+1):
                    f.write(str(t[i][j]) + ' ')
                f.write('\n')
            
            for i in range(0,N+1):
                for j in range(0, N+1):
                    f.write(str(c[i][j]) + ' ')
                f.write('\n')

        #create blank output file for the test case 
        output_file = os.path.join(test_dir, 'output.txt')
        with open(output_file, 'w') as f:
            f.write('')
        
        


