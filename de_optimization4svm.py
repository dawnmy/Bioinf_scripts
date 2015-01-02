import random
import numpy as np
from sklearn import preprocessing
from sklearn.svm import SVC
from numpy import sin

def rand(X,P,F,p):
	# R = list(np.random.permutation(P))
	(j, k, l, s) = tuple(random.sample(range(P),4))
	if j == p:
		j = s
	elif k == p:
		k = s
	elif l == p:
		l = s
	
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
	 all = read_data_table("breast-cancer.txt")
	 val, y = all["data"],all["label"]


	 # Open the file to store the best individual of every generation

	 clf = SVC(C=float(Cost[0]),gamma=float(Cost[1]),kernel='rbf')

	 acc = cross_validation.cross_val_score(clf,val, y, cv=5, scoring='accuracy')

	 return np.mean(acc)

# def func(xx):
# 	x = xx[0]
# 	y = xx[1]
# 	return 100 * (sin(x) ** 2 - sin(y)) ** 2 + (1 - sin(x)) ** 2

class DE:
	def __init__(self, NumVar = 2, Populations = 50, MutFa = 0.7, CroRate = 0.9, Generations = 100, NumRun = 1, XMin = [-2, -2], XMax = [2, 2], Func = func):
		self.N = NumVar	   # Number of variables
		self.P = Populations	  # Population size
		self.F = MutFa	 # Mutation factor
		self.Cr = CroRate	 # Crossover rate
		self.G = Generations	 # Number of Generations
		self.Run = NumRun	 # Number of test time
		# X_min = [0, 0]
		# X_max = [100, 8]
		self.X_min = XMin
		self.X_max = XMax
		self.func = Func

	def de(self):
		N = self.N
		P = self.P
		F = self.F
		Cr = self.Cr
		G = self.G
		Run = self.Run
		# X_min = [0, 0]
		# X_max = [100, 8]
		X_min = self.X_min
		X_max = self.X_max
		func = self.func
		for r in range(Run):
			Best = []
			g = 0	   
			# Initialize the generation
			X = np.array([[X_min[n]+random.random()*(X_max[n]-X_min[n]) for n in range(N)] for p in range(P)])
			
			for i in range(G):
				g += 1

				Y = []

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
					else:
						Tr = X[p,:]

					X[p,:] = Tr
					Y.insert(p,[list(X[p,]),func(X[p,])])
				Y = sorted(Y, key =lambda xxx:xxx[1], reverse=True)
				Best.append(Y[0])

			return Best

if __name__ == '__main__':
	de1 = DE(Populations = 20, Generations = 20, XMin = [0, 0], XMax = [32, 4])
	bestparameters = de1.de()
	generation = 1
	for parameter in bestparameters:

		print "Generation " + str(generation) + ": c = " + str(parameter[0][0]) + " and g = " + str(parameter[0][1]) + ", Acc = " + str(parameter[1])
		generation += 1
