# import statements
import sys
import cjson
import networkx as nx
import numpy
from scipy import sparse

# mention the path of tweets.txt
path = raw_input("enter the path where the tweets.txt is present including the file name")

# edges is a dictionary which stores the owner of the tweet and the list of users he mentions in the tweet
edges = {}
with open(path, 'r') as f:
	for line in f:
		data = cjson.decode(line)
		tweet_owner = data.get('user').get('screen_name')
		if not tweet_owner in edges :
			edges[tweet_owner] = set()
			for tweet_user in data.get('entities').get('user_mentions') :
				if tweet_user.get('screen_name')!= tweet_owner :
					edges.get(tweet_owner).update([tweet_user.get('screen_name')])
		else :
			for tweet_user in data.get('entities').get('user_mentions') :
				if tweet_user.get('screen_name')!= tweet_owner :
					edges.get(tweet_owner).update([tweet_user.get('screen_name')])

#creating the directed graph (where edge is created between user who created tweet and the user mentioned in the tweet)
G = nx.DiGraph();
edge_set = []
for e in edges :
	for f in edges.get(e) :
		edge_set.append((e,f))

# extracting the largest weakly connected component of the graph . Nodes is a list which stores the user names which are part of weakly connected components
G = nx.DiGraph(edge_set)
max = 0
for w in nx.weakly_connected_component_subgraphs(G):
	if max < len(w.nodes()) :
		max = len(w.nodes())
		Nodes = w.nodes()
#print max

# users_num is a dictionary which assigns a number to each node of weakly connected component
users_num = {}
i = 0
for e in Nodes :
	users_num[e] = i
	i = i+1

# L is a 1-0 matrix which stores whether an edge is present between two nodes or not
L = numpy.zeros(shape=(max,max))
for e in Nodes :
	if e in edges :
		for f in edges.get(e) :
			L[users_num.get(e)][users_num.get(f)] = 1
			
# a is authority 1-D array which stores authority values. Similarly h is Hubs array
a = numpy.ones(shape=(max))
h = numpy.ones(shape=(max))

# these arrays store hubs and authority values of previous iteration
previousa = numpy.ones(shape=(max))
previoush = numpy.ones(shape=(max))

# This is the basic HITS algorithm. Normalization is done based on the max element in the array. algorithm is continued until the error is < 0.00000001
flag = 0
while flag == 0 :
	flag = 1
	numpy.copyto(previousa, a)
	a = sparse.csr_matrix(L.T)*h
	maximum = a.max()
	a = [((x*1.0)/maximum) for x in a]
	numpy.copyto(previoush, h)
	h = sparse.csr_matrix(L)*a
	maximum = h.max()
	h = [((x*1.0)/maximum) for x in h]
	for i,j in zip(numpy.subtract(h,previoush),numpy.subtract(a,previousa)) :
		if numpy.absolute(i) > 0.00000001 or numpy.absolute(j) > 0.00000001 :
			flag = 0

# authorities and hubs are dictionaries which stores user screen name and their respective values
authorities = {}
hubs = {}
j=0
for x in Nodes :
	authorities[x] = a[j]
	hubs[x] = h[j]
	j = j+1

# sorting has been done to get top 20 hubs and authorities	
finalauthorities = {}
finalhubs = {}
finalauthorities=sorted(authorities, key=authorities.get, reverse=True)
finalhubs = sorted(hubs, key=hubs.get, reverse=True)

# This will print top 20 authorities
k=0
print "AUTHORITIES"
for j in finalauthorities :
	print j,"  : ",authorities.get(j)
	k=k+1
	if k >= 20 :
		break

# This will print top 20 hubs
print "HUBS"	
k=0
for j in finalhubs :
	print j,"  : ",hubs.get(j)
	k=k+1
	if k >= 20 :
		break
		