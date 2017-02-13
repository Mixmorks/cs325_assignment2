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

def align(d_cost, A, B):
   	#Generate empty array
   	a_edit_dist = [[0 for i in A] for j in B]
	
	#Fill like this:
	#0 1 2 3 4
	#1 0 0 0 0
	#2 0 0 0 0
	#3 0 0 0 0
	#4 0 0 0 0
	for i in range( len(A) ):
		a_edit_dist[0][i] = i

	for j in range( len(B) ):
	   	a_edit_dist[j][0] = j

	#Go through and fill the array based on the following:
	#If letter match, distance remains unchanged. Use distance from diagonal position
	#If letters do not match then distance becomes the minimum of surrounding blocks + effort to change that letter
	for j in range( 1, len(B) ):
		for i in range( 1, len(A) ):
			if( A[i] == B[j] ):
				a_edit_dist[j][i] = a_edit_dist[j-1][i-1]
			else:
				a_edit_dist[j][i] = min(a_edit_dist[j-1][i], a_edit_dist[j][i-1], a_edit_dist[j-1][i-1]) + d_cost[A[i]][B[j]]
	
	print a_edit_dist[len(A)][len(B)]
	

if __name__== "__main__":
	
   	f_cost = open('imp2cost.txt', 'r')
	f_data = open('imp2input.txt', 'r')
	f_output = open('imp2output.txt', 'w')

	d_cost = file_2_dict(f_cost)
	
	for line in f_data:
		A, B = line.split(',')
		B = B[:-1] #B will have a trailing newline, which needs to be removed

		align(d_cost, A, B)
		
	   
