
#Search Retrivel Component

#Query 1 "I love pie"
#Add 

#Retrieve Posting Lists
def retrievePostingList(queryStr):
	#Open Document
	f1 = open("./INDEX.txt","r",errors="ignore")
	#Split query by space
	listQuery = queryStr.split()
	#Create a dictionary to hold postings of each word { word-str:Postings-list }
	dictPostings =  dict() #cristina lopes {"cristina": [['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']],
						   # "lopes": [['DocID=2085', 'Pos=[16773, 16791]', 'Count=2', 'TDIF=2.0']]}
						   #
	#Build dictPostings by finding the postings for each word 
	for word in listQuery:
		while True:
			if(parseLineFromWord(f1.readline()) == word):
				dictPostings[word] = 
				break

#Read word from line
def parseLineForWord(str1):
	#Parse the word from the line
	#EX: Word=aaainji:Postings=[['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']]
	#	 return aaainji
	#	 [5:] , read up to :
	indexColon = word.find(':')
	return str1[5:indexColon]

def getListPostingsFromLine(str1):
	#Parse the posting from the line
	#EX: Word=aaainji:Postings=[['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']]
	#	 return [['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']]
	indexColon = str1.find('Postings=')
	return str1[indexColon + len("Postings="):]

def createPostingListFromStr(strPosting):

	postingsList = list()
	while True:
		indexColon = str1.find("'DocID")
