import random
import numpy as np
from sklearn import preprocessing
from sklearn.svm import SVC

def rand(X,P,F,p):
    R = list(np.random.permutation(P))
    (j, k, l, u, v) = (R[i] for i in range(5))
    if j == p:
        j = R[6]
    elif k == p:
        k = R[6]
    elif l == p:
        l = R[6]
    elif u == p:
        u = R[6]
    elif v == p:
        v = R[6]
    M = X[j,:] + F*(X[k,:]-X[l,:])
    return M

def read_data_table(inf):
    inputfile = inf

    datamatrix = np.array([map(float,line.split()[1:]) for line in open(inputfile).readlines()])
    min_max_scaler = preprocessing.MinMaxScaler()
    data_scaled = min_max_scaler.fit_transform(datamatrix)

    label = np.array(map(int,[line.split()[0] for line in open(inputfile).readlines()]))

    dataform = {"data":data_scaled,"label":label}

    return(dataform)
def func(Cost):
    from sklearn import cross_validation

    markers = [45,63,68,77]
    # top100 = read_data_table("top100.txt")
    # jorth100 = read_data_table("jo_bwa_19seed_top100.txt")
    #
    # val, y = top100["data"][:,markers],top100["label"]
    # X_train, X_test, y_train, y_test = val,val,y,y
    # Jx_test, Jy_test = jorth100["data"][:,markers],jorth100["label"]
    # Train = np.vstack([X_train, Jx_test])
    # Label = np.append(y_train,Jy_test)

    top100 = read_data_table("top100.txt")
    jorth100 = read_data_table("jo_bwa_19seed_top100.txt")
    # all = read_data_table("breast-cancer.txt")
    val, y = top100["data"][:,markers],top100["label"]
    # val, y = all["data"],all["label"]


    # Open the file to store the best individual of every generation

    clf = SVC(C=float(Cost[0]),gamma=float(Cost[1]),kernel='linear')

    acc = cross_validation.cross_val_score(clf,val, y, cv=4, scoring='accuracy')

    return np.mean(acc)

N = 2       # Number of variables
P = 20      # Population size
F = 0.5     # Mutation factor
Cr = 0.9     # Crossover rate
G = 10     # Number of Generations
Run = 1     # Number of test time
X_min = [0, 0]
X_max = [100, 8]
Best = []
for r in range(Run):
    g = 0       # Initialize the generation
    X = np.array([[X_min[n]+random.random()*(X_max[n]-X_min[n]) for n in range(N)] for p in range(P)])
    # for p in range(P):
    #     for n in range(N):

    Y = []
    for i in range(G):
        g += 1


        for p in range(P):

            # DE mutation
            V = rand(X,P,F,p)

            # Bound check
            for n in range(N):
                if V[n] > X_max[n]:
                    V[n] = 2 * X_max[n] - V[n]
                if V[n] < X_min[n]:
                    V[n] = 2 * X_min[n] - V[n]

            # Crossover
            U = []
            jrand =random.randint(0,N-1)
            for n in range(N):
                R1 = random.random()
                if R1 < Cr or n == jrand:
                    U.insert(n,V[n])
                else:
                    U.insert(n,X[p,n])

            # Selection
            if func(U) > func(X[p,]) or (func(U) == func(X[p,]) and U[0] < X[p,0]):
                Tr = np.array(U)
                # Ac = func(Tr)
            else:
                Tr = X[p,:]
                # Ac = func(Tr)

            X[p,:] = Tr
        # Y.insert(i,[Tr,Ac])
            print Tr, func(Tr)


            # print U
        # Best.append([r,i,max(Y)])
    # for line in list(Y):
    #     print line
