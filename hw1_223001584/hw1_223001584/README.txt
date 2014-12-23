README FILE

Rajashree Rao Polsani
UIN : 223001584
Information Storage and Retrieval : HW1


Procedure to run the program :

1.	In the command line enter "python hw_source_code.py"
2.  Initially path for the data folder is asked. Enter the entire path including the data folder name.
	(path example : C:\IRass1\nsf-award-abstracts)
3. 	Index for both the models , boolean retrieval model and vector space model, are built at a time. Once the index has been built it will be indicated on the terminal
	Index will be built only once.
4.	Enter   0 	  - for boolean retrieval model
		    1 	  - for vector space model
			exit  - for terminating the program
5.  Once the model has been selected, enter the query.
6.  For boolean retrieval model matching documents are listed
	For vector space model matching documents as well as their cosine similarity values are listed.
	

Approximate time taken to build index : 
	on linux2.cs.tanu.edu : 150 sec
	on windows8 (intel i7) : 70 sec