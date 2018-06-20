import time
import signal
import sys
max_clique = set() 

def findPivot(PuX, P, dic):
# choose the pivot in S as the vertex with the highest number of neighbors in S
	pivot = -1
	pivot_nbrs = set()
	for u in PuX:
		u_nbrs = nbrs(u, P, dic)
		if(len(u_nbrs)>=len(pivot_nbrs)):
			pivot = u
			pivot_nbrs = u_nbrs

	return pivot, pivot_nbrs

def nbrs(v, S, dic):
	return dic[v].intersection(S)

def BronKerbosch(P,R,X, dic, indent):
	# print("R,P,X")
	print(indent,R,P,X)
	if (len(P)==0 and len(X)==0):
		# print("Maximal: ")
		# print(R)
		global max_clique
		if(len(R)>len(max_clique)):
			max_clique = R
			print("max_clique ", max_clique)
		return 
	pivot, pivot_nbrs = findPivot(P.union(X), P, dic)
	print("Pivot:", pivot)
	# print("Pivot neighbors:",pivot_nbrs)
	# pivot_nbrs = 
	for v in P.difference(pivot_nbrs):
		v_nbrs = nbrs(v, P, dic)
		BronKerbosch(P.intersection(v_nbrs), R.union(set([v])), X.intersection(v_nbrs), dic, indent+'  ')
		P.discard(v)
		X.add(v)
	
def output():
	global max_clique, start, outfile
	print(max_clique)
	end1 = time.time()
	print("Total vertices in the clique: ", len(max_clique))
	print("exacution time: ",end1-start)

	with open(outfile, "w") as f:
		for p in max_clique:
			# print(len(set(dic[key])))
			f.write(str(p)+'\n')
	end2 = time.time()
	print("output time: ",end2-end1)

def handler(signum, frame):
	output()
	print("SIGALRM")
	sys.exit()

#Sets an handler function, you can comment it if you don't need it.
signal.signal(signal.SIGALRM,handler) 
#If uncaught will terminate your process.
signal.alarm(170) 

start = time.time()

infile = "test2.txt"
outfile = "output.txt"

dic = {}
with open(infile, "r") as f:
	for i,line in enumerate(f):
		vertices = line.split()
		v1 = int(vertices[0])
		v2 = int(vertices[1])
		# if(i>1000 and i<1050):
		# 	print(v1, ' ', v2)
		# 	print(dic[v1])
		if(v1 in dic):
			dic[v1].add(v2)
		else:
			dic[v1] = set([v2])
		if(v2 in dic):
			dic[v2].add(v1)
		else:
			dic[v2] = set([v1])

	R = set([])
	P = set(dic.keys())
	X = set([])

	# print(dic[4])
	# print(nbrs(4, P, dic))

	maximum_clique = BronKerbosch(P,R,X, dic, '')
	output()
