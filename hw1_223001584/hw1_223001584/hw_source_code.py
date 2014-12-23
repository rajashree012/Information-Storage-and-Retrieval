# import statements
import glob
import os
import math
import fnmatch
import time

# mention the path of data folder 
path = raw_input("enter the path where the nsf-award-abstracts folder is present")

# files_list stores the list of file names including their path
files_list = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(path)
    for f in fnmatch.filter(files, '*.txt')]
print "total number of files"
print len(files_list)

start_time = time.time()

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
i = 0
for file_name in files_list :
    with open(file_name,'r') as f:
        for line in f:
            for words in line.split():
                for character in words :
                    if not(character.isalnum() or character.isspace()) :
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
#print len(doc_freq)
#print len(term_freq)

print "time taken :",time.time() - start_time, "seconds"

# scores is a list in which magnitude of each document vector is stored
scores = [0]*len(files_list)
for k in term_freq :
    for l in term_freq.get(k) :
        scores[l] = scores[l] + math.pow((1 + math.log(term_freq.get(k)[l],10)) * (math.log(len(files_list)/(doc_freq.get(k)*1.0),10)),2)
for a in range(0,len(files_list)) :
    scores[a] = math.sqrt(scores[a])

exit_flag = 0
while exit_flag == 0 :
    query_flag = 0
    # taking input from the users
    print "The index for both boolean retrieval model and vector space model has been built."
    input_var = raw_input("Enter 0 for boolean retrieval model or 1 for vector space model or exit for terminating the program")
    if input_var == "exit" :
        break
        exit_flag = 1
    query_list = {}
    if (input_var == '0' or input_var == '1') :
        # query list stores the tokens of the query
        query = raw_input("enter the query")
        for wordq in query.split():
            for character in wordq :
                if not(character.isalnum() or character.isspace()) :
                     wordq=wordq.replace(character," ")
            for word in wordq.split() :
                if word.lower() not in tokens :
                    print "no matching document found"    
                    # if one of the tokens in query is not present in the dictionary then nothing is returned
                    query_flag = 1
                    break;
                else : 
                    if word.lower() in query_list :
                        query_list[word.lower()] = query_list[word.lower()] + 1
                    else :
                        query_list[word.lower()] = 1
    else : 
        print "invalid command"
    
    # when the query is devoid of any alphanumeric characters then the following if is executed
    if (len(query_list) == 0 and (input_var == '0' or input_var == '1') and query_flag != 1) :
        print "no matching document found"
        query_flag = 1

    #print query_list

    # following if statement is executed if vector space model is selected
    if (query_flag == 0 and input_var == '1') :
        # magnitude of query
        query_magn = 0
        for q in query_list :
            query_magn = query_magn + math.pow(query_list[q],2)
        query_magn = math.sqrt(query_magn)
        
        # calculations_list is a dictionary which stores the sum of dot product query vector and document vector for each document
        calculations = [0]*len(files_list)
        for aa in query_list :
            for bb in term_freq.get(aa) :
                calculations[bb] = calculations[bb] + (1 + math.log(term_freq.get(aa)[bb],10)) * (math.log(len(files_list)/(doc_freq.get(aa)*1.0),10))*query_list[aa]
                
        calculations_list = {}
        for aaa in range(0,len(files_list)) :
            calculations[aaa] = calculations[aaa]/(scores[aaa] * query_magn * 1.0)
            calculations_list[aaa] = calculations[aaa]

        #final vector stores document scores in decreasing order
        final = []
        final=sorted(calculations_list, key=calculations_list.get, reverse=True)
      
        # top 50 ranked documents of vector space model are printed
        count = 0
        for f in final :
            if count >= 50 or calculations_list[f] <= 0.0:
                if count == 0 :
                    print "query present in all the documents"
                break
            print dict_docid_docname[f]," ","[",calculations_list[f],"]"
            count = count + 1

    # following if statement is executed if boolean retrieval model is selected 
    if (query_flag == 0 and input_var == '0') :
        common = set()
        common = tokens[query_list.keys()[0]]
        for q in query_list :
            common = common.intersection(tokens[q])
        for c in common :
            print dict_docid_docname[c]
        if len(common) == 0 :
            print "no matching document found"

