import csv

def file_2_dict(f_cost):
   	reader = csv.reader(f_cost, delimiter=',')
	
	#Break the matrix into a 2D array
	a = []
	for row in reader:
		a.append(row)

	#Creates a 2D Dictionary from the 2D array
	d = {}
	for i in range(1, len( a )):
		d_temp = {}
		for j in range(1, len( a[0] )):
			d_temp[a[0][j]] = int(a[i][j])
		d[a[i][0]] = d_temp

	#i.e. d['A']['T'] will return 2, as will d['T']['A']
	return d

def edit_distance(d_cost, A, B):
	#The alignment table uses string A and B with a - prepended to it.
	A = '-' + A
	B = '-' + B

   	#Generate empty array
   	a_edit_dist = [[0]*len(A) for j in B]

	#Fill like this:
	#0 1 2 3 4
	#1 0 0 0 0
	#2 0 0 0 0
	#3 0 0 0 0
	#4 0 0 0 0
	a_edit_dist[0][0] = 0
	for i in range( 1, len(A) ):
		a_edit_dist[0][i] = a_edit_dist[0][i-1] + d_cost[A[i]]['-']

	for j in range( 1, len(B) ):
	   	a_edit_dist[j][0] = a_edit_dist[j-1][0] + d_cost[B[j]]['-']

	#Go through and fill the array based on the following:
	#For each letter the effort is the minimum of surrounding blocks + effort to change that letter
	#Keep in mind that matching letters have a cost of 0. i.e d_cost['A']['A'] = 0
	for j in range( 1, len(B) ):
		for i in range( 1, len(A) ):
		   	temp = 0
			if A[i] == B[j]:
				temp = a_edit_dist[j-1][i-1]
			else:
			   	temp = a_edit_dist[j-1][i-1] + d_cost[B[j]][A[i]]

			a_edit_dist[j][i] = min( temp, a_edit_dist[j-1][i] + d_cost[B[j]]['-'], a_edit_dist[j][i-1] + d_cost['-'][A[i]])


	for u in range(len(B)):
		print a_edit_dist[u]

	return a_edit_dist
	
def align(A, B, a_edit_dist):
	#The theory here is that we'll start at the bottom right corner for the solved case
	#and step into the direction of lowest cost until we hit the top left corner building the string as we go.
	aligned_A = ""
	aligned_B = ""

	#i = len(B)
	#j = len(A)
	i = 0
	j = 0

	while i < len(B) and j < len(A):
		min_cost = min(a_edit_dist[i+1][j], a_edit_dist[i+1][j+1], a_edit_dist[i][j+1])
		#Diagonal step means we either swapped or the letters are equal
		#Order of these matters! A diagonal step is preferred as it implies no change
		print "Checking a_edit_dist [" + str(i) + "][" + str(j) + "]"
		print aligned_A
		print aligned_B
		if min_cost == a_edit_dist[i+1][j+1]:
			aligned_A = aligned_A + A[j]
			aligned_B = aligned_B + B[i]
			i = i + 1
			j = j + 1

		#Step left means a gap on string A was matched with a letter at string B	
		elif min_cost == a_edit_dist[i+1][j]:
			aligned_A = aligned_A + '-'
			aligned_B = aligned_B + B[i]
			i = i + 1

		#Step up means a gap on string B was matched with a letter from string A
		elif min_cost == a_edit_dist[i][j+1]:
			aligned_A = aligned_A + A[j]
			aligned_B = aligned_B + '-'
			j = j + 1


	if j < len(A):
		aligned_A = aligned_A + A[j]
		aligned_B = aligned_B + '-'*(len(A)-j)

	if i < len(B):
		aligned_A = aligned_A + '-'*(len(B)-i)
		aligned_B = aligned_B + B[i:]
	
	print aligned_A
	print aligned_B
	return aligned_A, aligned_B
		
if __name__== "__main__":
	
   	f_cost = open('imp2cost.txt', 'r')
	f_data = open('imp2input.txt', 'r')
	f_output = open('imp2output.txt', 'w')

	d_cost = file_2_dict(f_cost)

	for line in f_data:
		A, B = line.split(',')
		B = B[:-1] #B will have a trailing newline, which needs to be removed
		
		#Generate the edit distance array and use that to build our aligned strings
		a_edit_dist = edit_distance(d_cost, A, B)

		a_A, a_B = align(A, B, a_edit_dist)
		f_output.write(a_A + "," + a_B + ":" + str(a_edit_dist[len(B)][len(A)]) + "\n")
