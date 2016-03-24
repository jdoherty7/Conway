import time
import os
import random

"""

This is a script that creates a cellular automaton.
In this version, it runs Conway's Game of Life, which
is interesting becuase it is based off of evolutionary 
principles and can run a turing complete machine 
within the simulation.

"""


#create an array
def create(n):
	new = []
	for i in range(n):
		new.append([])
		for j in range(n):
			new[i].append(0)
			j = j + 1
		i = i + 1
	return new

#set the initial conditions
def initial():
	start = create(10)
	start[2][3] = 1
	start[4][6] = 1
	start[7][4] = 1
	return start

#create a randomized initial conditions and array size
def rand_initial():
	start = create(random.randrange(12, 23))
	for i in range(len(start)):
		for j in range(len(start)):
		#change this to higher to create lower probability of 1s
			hold = random.randrange(2,4)
			if hold == 3:
				start[i][j] = 1
	return start


#create a state matrix showing number of living neighbors
#that a cell has at some given point
def adjacency_array(start):
	y = len(start)
	end = create(y)	
	for i in range(1,y-1):
		for j in range(1,y-1):
			above = start[i-1][j-1] + start[i-1][j] + start[i-1][j+1]
			below = start[i+1][j-1] + start[i+1][j] + start[i+1][j+1]
			sides = start[i][j-1] + start[i][j+1]
			end[i][j] = above + below + sides
	x = y-1
	for i in range(1, y-1):
		#top row
		down = start[1][i-1] + start[1][i] + start[1][i+1]
		side = start[0][i-1] + start[0][i+1]
		end[0][i] = down + side
		#bottom row
		up = start[x-1][i-1] + start[x-1][i] + start[x-1][i+1]
		lr = start[x][i-1] + start[x][i+1]
		end[x][i] = up + lr
		#first column
		right = start[i-1][1] + start[i][1] + start[i+1][1]
		updown = start[i-1][0] + start[i+1][0]
		end[i][0] = right + updown
		#last column
		left = start[i-1][x-1] + start[i][x-1] + start[i+1][x-1]
		updwn = start[i-1][x] + start[i+1][x]
		end[i][x] = left + updwn

	#special cases for corners
	end[0][0] = start[1][0] + start[1][1] + start[0][1]
	end[x][x] = start[x-1][x-1] + start[x][x-1] + start[x-1][x]
	end[x][0] = start[x][1] + start[x-1][1] + start[x-1][0]
	end[0][x] = start[1][x] + start[0][x-1] + start[0][x-1]	
	return end

#rules for conway's game of life
def life(initial, state, final):
	length = len(state)
	#any live cell with fewer than two neighbors dies by underpopulation
	#will also die from overpopulation
	for i in range(length):
		for j in range(length):
			if state[i][j] < 2 or state[i][j] > 3:
				final[i][j] = 0
	#things are born as if by reproduction
			if state[i][j] == 3:
				final[i][j] = 1
	#things persist if they only have two or three neighbors
			if initial[i][j] == 1 and (state[i][j] == 2 or state[i][j] == 3):
				final[i][j] = 1
	return final


#discontinued in life
def move(first, next):
	for j in range(len(first)):
		for i in range(len(first[j])):
		#move particle right
			if first[j][i] == 1:
				if i + 1 >= len(first[j]):
					next[j][0] = 1
				else:
					next[j][i+1] = 1
	return next

#discontinued in life
def birth(init, final):
	for j in range(len(init)):
		for i in range(0, len(init)-3):
			if init[j][i] == 1 and init[j][i+2] == 1:
				final[j][i] = 1
				final[j][i+1] = 1
				final[j][i+2] = 1
	#let things be born at boudaries
	#make sure the old things are still there	
		if init[j][1] == 1:
			final[j][0] = 1
			final[j][1]= 1
		if init[j][len(init)-2] == 1:
			final[j][len(init)-2] = 1
			final[j][len(init)-1] = 1
	return final

#let things die from overpopulation
#discontinued in life version
def death(init, final):
	for j in range(len(init)):
		for i in range(0, len(init)-3):
			if init[j][i] == 1 and init[j][i+2] ==1:
				final[j][i] = 0
				final[j][i+1] = 0
				final[j][i+2] = 0
	return final

#run rules, which take a matrix and turns it into another
#matrix based on some rules. life function has all rules 
#for conway's game of life
def rules(first):
	#create new array same size as first one
	#only need one length because it is square
	next = create(len(first))
	state = adjacency_array(first)
	next = life(first, state, next)
	
	#random initial rules for test
	#these were previous used rules for a different cellular
	#automotan that behaved with different rules.
	#next = move(first, next)
	#next = birth(first, next)
	#next = death(first, next)
	
	return next

#transform matrix into an easier to view format
#1s are 0s and 0s are 1s
def xform(inside, x):
	z = len(inside)
	for i in range(z):
		for j in range(z):
			if inside[i][j] == 1:
				inside[i][j] = 0
			else:
				inside[i][j] = 1
	return inside

def Main():
	start = rand_initial()
	var = 0
	length = len(start)
	while var <= 50:
		next = rules(start)
		print "Time: " + str(var)	
		#new = xform(next, 'X')
		for i in range(length):		
			print next[i]
		print "LOOK AT IT WORKING!"
		numbers = adjacency_array(next)
		#for j in range(len(numbers)):
		#	print numbers[j]
		time.sleep(.7)
		os.system('cls' if os.name == 'nt' else 'clear')
		start = next
		var = var + 1

if __name__ == "__main__":
	Main()
