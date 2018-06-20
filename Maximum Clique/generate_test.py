from random import randint

with open('test1.txt', "w") as f:
	for i in range(2000):
		for j in range(i+1,2000):
			v1 = str(i)
			v2 = str(j)
			f.write(v1+' '+v2+'\n')
	for i in range(2400000):
		v1 = str(randint(0, 82168))
		v2 = str(randint(0, 82168))
		f.write(v1+' '+v2+'\n')
