import numpy as np
x=[[0 for i in range(5)] for j in range(5)]


def check_pos_reward(i,j):
	reward=0
	if i-1 < 0 or j-1 < 0 or i+1 > 4 or j+1 > 4:
		reward = -1
	return reward

n = 20
count = 0
pos_i = 0
pos_j =0 
act = None
while count < n:
		reward = 0
		if pos_i-1<0:
			left=(x[pos_i][pos_j],-1)
		else:
			left=(x[pos_i][pos_j-1],0)
	
		if pos_j+1>4:
			right=(x[pos_i][pos_j],-1)
		else:
			right=(x[pos_i][pos_j+1],0)
	
		if pos_i-1<0:
			top=(x[pos_i][pos_j],-1)
		else:
			top=(x[pos_i-1][pos_j],0)

		if pos_i+1>4:
			down=(x[pos_i][pos_j],-1)
		else:
			down=(x[pos_i+1][pos_j],0)


		surround = [('l',left), ('r',right), ('t',top), ('d',down)]

		if pos_i==0 and pos_j==1:
			reward = 10
			surround =[('j',(x[4][1],10))]
		if pos_i==0 and pos_j==3:
			reward = 5
			surround =[('j',(x[2][3],5))]


		max_val = -100
		for flag,tup_ in surround:
			surr_,rew_ = tup_
			val = 1.0/4*(rew_+0.9*surr_)
			print "val ",val
			if(val > max_val):
				max_val = val
				act = flag
		x[pos_i][pos_j] = max_val
		

		# decide next move
		if pos_i==0 and pos_j==1:
			pos_i=4
			pos_j=1
		elif pos_i==0 and pos_j==3:
			pos_i=2
			pos_j=3
		else:
			flag = np.random.choice(['l','r','t','d'], p=[1.0/4,1.0/4,1.0/4,1.0/4])
			if flag=='l' and pos_j-1>=0:
				pos_j=pos_j-1
			if flag=='r' and pos_j+1<=4:
				pos_j=pos_j+1 
			if flag == 't' and pos_i-1>=0:
				pos_i= pos_i -1
			if flag=='d' and pos_i+1<=4:
				pos_i = pos_i + 1

		print x
		print "--------",flag


print x