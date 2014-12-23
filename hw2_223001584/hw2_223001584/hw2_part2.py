# import statements
import sys
import networkx as nx
import numpy
from scipy import sparse
import fnmatch
from sklearn.svm import SVC
from sklearn.svm import LinearSVC

# This functions creates pairs of documents which correspond to same query and calculates it's relevance value
def create_pairs (path) :
	# relevance is a dictionary of queryId and dictionary of line number in the file(which indirectly corresponds to document) and relevance
	relevance = {}
	# input_raw_features is 2D matrix which stores feature values of each document in the file 
	input_raw_features = numpy.array([])
	with open(path, 'r') as f:
		for num,line in enumerate(f,1):
			query = line.split()[1].split(':')[1]
			if query not in relevance :
				relevance[query] = {}
				relevance[query] = {num-1 : line.split()[0]}
				temp=numpy.zeros(shape=(40))
				for i in range(2,42):
					temp[i-2]=(line.split()[i].split(":")[1])
				input_raw_features=numpy.append(input_raw_features,temp)
			else :
				relevance.get(query)[num-1] = line.split()[0]
				temp=numpy.zeros(shape=(40))
				for i in range(2,42):
					temp[i-2]=(line.split()[i].split(":")[1])
				input_raw_features=numpy.append(input_raw_features,temp)
	input_raw_features=numpy.reshape(input_raw_features,(num,40))

	# input_raw_features is 2D matrix which stores difference in feature values of two docs of same query. 
	# input_faetures is an array to be fed in SVM
	input_features = numpy.array([])
	# output_class is an array which contains +1 or -1 corresponding two documents after comparing the relevance
	output_class = numpy.array([])
	count = 0
	for q in relevance :
		for i in relevance.get(q) :
			for j in relevance.get(q) :
				if relevance.get(q).get(i) != relevance.get(q).get(j) :
					temp = numpy.zeros(shape=(40))
					temp = numpy.subtract(input_raw_features[i],input_raw_features[j])
					input_features=numpy.append(input_features,temp)
					if relevance.get(q).get(i) < relevance.get(q).get(j) :
						output_class=numpy.append(output_class,-1)
					else : 
						output_class=numpy.append(output_class,1)
					count = count + 1
	input_features=numpy.reshape(input_features,(count,40))
	return (input_features,output_class)

# This code will iterate 3 times corresponding to 3 folders
num_folder = 1
# Best C values are found for good accuracy
c = [0.04,9.0,0.004]

while num_folder <= 3 :
	print "Now train and test for folder ",num_folder
	# training the data by sending it to svc
	path = raw_input("enter the path where the train.txt file is present including the file name")

	svc = SVC(kernel='linear',C=c[num_folder-1])
	output = create_pairs (path)
	svc.fit(output[0],output[1])

	# sorting the feature weights by their absolute value
	absolute_weights = []
	for s in svc.coef_[0] :
		absolute_weights.append(numpy.absolute(s))
	weights_original = {}
	count = 1
	for s in svc.coef_[0] :
		if count>=1 and count<=5 :
			weights_original[count] = s
		if count>=6 and count<=37 :
			weights_original[count+5] = s
		if count>=38 and count<=40 :
			weights_original[count+6] = s
		count = count+1
	weights = {}
	count = 1
	for s in absolute_weights :
		if count>=1 and count<=5 :
			weights[count] = s
		if count>=6 and count<=37 :
			weights[count+5] = s
		if count>=38 and count<=40 :
			weights[count+6] = s
		count = count+1
	sorted_weights = []
	sorted_weights=sorted(((v,k) for k,v in weights.iteritems()), reverse=True)
	i = 0;
	for v,k in sorted_weights:
		print "feature :",k," : ",weights_original[k]
		i = i+1
		if i >= 10 :
			break

	#testing
	path = raw_input("enter the path where the test.txt file is present including the file name")
	output = create_pairs (path)
	print "accuracy :",svc.score(output[0],output[1])*100.0
	
	num_folder = num_folder + 1