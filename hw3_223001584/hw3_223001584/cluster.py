# import statements
import glob
import os
import math
import fnmatch
import time
import tweepy
from random import randrange
import numpy
import HTMLParser
from nltk.corpus import stopwords
import pylab as pl

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
print "retrieving the tweets"
# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key=""
consumer_secret=""

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#api = tweepy.API(auth)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# creating files for each query ie each document
# files_list stores the list of file names including their path
files_list = []
list_of_queries = ["#katyperry", "#katycats", "#darkhorse", "#iHeartRadio", "#ladygaga", "#TaylorSwift", "#sxsw", "Rolling Stone","@DwightHoward", "#rockets", "jeremy lin", "toyota center", "kevin mchale", "houston nba", "James Harden", "linsanity", "Jan Koum", "WhatsApp", "#SEO", "facebook", "#socialmedia", "Zuckerberg", "user privacy", "#Instagram","Obama", "#tcot", "Russia", "Putin", "White House", "Ukraine", "Rand Paul", "foreign policy"]
count1 = 0
for query in list_of_queries :
    count1 = count1 + 1
    filename = str(count1)+ ".txt"
    files_list.append(filename)
    f = open(filename,'w')
    query = list_of_queries[count1-1],"-RT"
    result = api.search(q = query, count=50, lang='en')
    for t in result['statuses']:
        h=HTMLParser.HTMLParser()
        tweetstring=h.unescape(t['text'])
        tweetstring=tweetstring.encode('ascii','ignore').lower()
        f.write(tweetstring)
        f.write('\n')
    f.close()


print "total number of files"
print len(files_list)

start_time = time.time()
print "building index ..."
# dict_docid_docname dictionary stores mappings of a unique doc id for each text file in the folder
j=0
dict_docid_docname = {}
for z in files_list:
    dict_docid_docname[j]=z.split("\\")[-1].split("/")[-1].split('.')[0]
    j=j+1

# tokens dictionary stores tokens and set of doc ids in which the token is present
tokens = {}
# term_freq dictionary stores tokens and frequency of each token in each document
term_freq = {}
# doc_freq dictionary stores tokens and its document frequency
doc_freq = {}

# 'i' acts like document counter
# each line from every file is read
# here all the non-alphanumeric characters are replaced by space and then split command is used in order to generate the tokens
# Term frequency of each term in every document is also simultaneously calculated
# all the stopwords and urls are removed
i = 0
stop = stopwords.words('english')
for file_name in files_list :
    with open(file_name,'r') as f:
        for line in f:
            for words in line.split():
                if not words.split(":")[0] == "http" :
                    if words not in stop :
                        #if wordnet.synsets(words):
                        for character in words :
                            if not(character.isalnum() or character.isspace() or character=='#' or character=='@') :
                                words=words.replace(character," ")
                        for word in words.split() :
                            if word.lower() in tokens :
                                tokens.get(word.lower()).update([i])
                                if i in term_freq.get(word.lower()) :
                                    term_freq.get(word.lower())[i] = term_freq.get(word.lower())[i] + 1
                                else :
                                    term_freq.get(word.lower())[i] = 1
                            else :
                                tokens[word.lower()] = set([i])
                                term_freq[word.lower()] = {i : 1}
    i = i+1
    
# Document frequency of each token is calculated
for key in tokens :
    doc_freq[key] = len(tokens.get(key))
#print len(tokens)

print "time taken :",time.time() - start_time, "seconds for building index"

# scores is a list in which magnitude of each document vector is stored
scores = [0]*len(files_list)
for k in term_freq :
    for l in term_freq.get(k) :
        scores[l] = scores[l] + math.pow((1 + math.log(term_freq.get(k)[l],10)) * (math.log(len(files_list)/(doc_freq.get(k)*1.0),10)),2)
for a in range(0,len(files_list)) :
    scores[a] = math.sqrt(scores[a])

# creating a dictionary where a document and tf-idf corresponding to each token in token-frequency is stored
doc_tf_idf = {}

for k in term_freq :
    for x in range(0,len(files_list)) :
        if x in term_freq.get(k) :
            if x in doc_tf_idf :
                doc_tf_idf.get(x).append(((1 + math.log(term_freq.get(k)[x]*1.0,10)) * (math.log(len(files_list)/(doc_freq.get(k)*1.0),10)))/scores[x])
            else :
                doc_tf_idf[x] = []
                doc_tf_idf.get(x).append(((1 + math.log(term_freq.get(k)[x]*1.0,10)) * (math.log(len(files_list)/(doc_freq.get(k)*1.0),10)))/scores[x])
        else : 
            if x in doc_tf_idf :
                doc_tf_idf.get(x).append(0)
            else :
                doc_tf_idf[x] = []
                doc_tf_idf.get(x).append(0)

purity = 0
    
# k means clustering
RSS_Values = []
k_values = [2,4,6,8]
best_RSS = []
best_purity = 0
best_centroids = {}
for k_value in k_values :
    number_of_iter = 0
    while (number_of_iter < 50) :
        # randomely picking up centroids
        centroids = {}
        for k in range(0,int(k_value)) :
            xxx = randrange(len(files_list)-1)
            #print xxx
            centroids[k]=doc_tf_idf.get(xxx)
        previous_centroid_points = numpy.zeros(len(files_list))
        current_centroid_points = numpy.zeros(len(files_list))
       
        # starting the iterations
        flag = 0
        iteration = 0
        while flag == 0 :
        # for every document vector
            for point in doc_tf_idf :
                
                # finding magnitude of centroid vector
                magn = 0
                for x in range(0,len(centroids.get(0))) :
                    magn = magn + math.pow(centroids.get(0)[x],2)
                magn = math.sqrt(magn)
                if magn != 0 and scores[point] != 0:
                    maximum = numpy.sum(numpy.divide(numpy.multiply(centroids.get(0),doc_tf_idf.get(point)),(scores[point]*magn)))
                else :
                    maximum = 0
                    
                # finding the centroid which is closest to the point using cosine similarity
                current_centroid_points[point] = 0
                for centre in centroids :
                    magn = 0
                    for x in range(0,len(centroids.get(centre))) :
                        magn = magn + math.pow(centroids.get(centre)[x],2)
                    magn = math.sqrt(magn)
                    if magn != 0 and scores[point] != 0:
                        temp = numpy.sum(numpy.divide(numpy.multiply(centroids.get(centre),doc_tf_idf.get(point)),(scores[point]*magn)))
                    else :
                        temp = 0
                    if temp > maximum :
                        maximum = temp
                        current_centroid_points[point] = centre
            
            # recalculating the new centroids
            count = int(k_value)*[0]
            for k in range(0,int(k_value)) :
                centroids[k]=len(term_freq)*[0]
            for y in range(0,len(files_list)) :
                centroids[int(current_centroid_points[y])] = numpy.add(centroids.get(int(current_centroid_points[y])),doc_tf_idf.get(y))
                count[int(current_centroid_points[y])] = count[int(current_centroid_points[y])] + 1
            for k in range(0,int(k_value)) :
                magn = 0
                for x in range(0,len(centroids.get(k))) :
                    magn = magn + math.pow(centroids.get(k)[x],2)
                magn = math.sqrt(magn)
                #if count[k] != 0 :
                # normalising the centroid
                if magn != 0 :
                    centroids[k] = numpy.divide(centroids[k],magn)
                    
            # checking whether the centroids have changed
            flag = 1
            for x in range(0,len(files_list)) :
                if previous_centroid_points[x] != current_centroid_points[x] : 
                    flag = 0
                    break
                
            iteration = iteration + 1
            
            # updating new centroids
            for x in range(0,len(files_list)) :
                previous_centroid_points[x] = current_centroid_points[x] 
          
        # RSS calculations
        RSS = 0
        for doc in range(0,len(files_list)) : 
            sums = 0
            for component in range(0,len(term_freq)) :
                sums = sums + math.pow(doc_tf_idf.get(doc)[component]-centroids.get(current_centroid_points[doc])[component],2)
            RSS = RSS + sums
        if best_RSS > RSS :
            best_RSS = RSS
    
        # purity
        if k_value == 4 :
            actual_centroid_points = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3]
            purity = 0
            cluster_centroid = {}
            for i in range(0,k_value) :
                cluster_centroid[i] = [0,0,0,0]
            for j in range(0,len(current_centroid_points)) :
                cluster_centroid.get(int(current_centroid_points[j]))[actual_centroid_points[j]] = cluster_centroid.get(int(current_centroid_points[j]))[actual_centroid_points[j]] + 1
            for i in range(0,k_value) :
                purity = purity + max(cluster_centroid.get(i))
            purity = purity*1.0/32
            if best_purity < purity :
                best_purity = purity
                best_centroids = cluster_centroid
            
        number_of_iter = number_of_iter + 1
    print "\n"  
    print str(k_value) + "clusters"
    print "RSS value = " + str(best_RSS)
    if k_value == 4 :
        print "purity = " + str(best_purity)
        print "this dictionary includes no.of of documents in each cluster and how they are distributed within the original classes"
        print best_centroids
        
    RSS_Values.append(best_RSS)
    
# drawing the graph
pl.plot(k_values, RSS_Values)
pl.show()