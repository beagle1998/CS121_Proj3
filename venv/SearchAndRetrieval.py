
#Search Retrivel Component

#Query 1 
#Steps:

#	1) Type in Search:
#	"cristina lopes"

#	2) Get Postings Dictionary
#	cristina lopes 
#	{"cristina": [['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']],
#   "lopes": [['DocID=2085', 'Pos=[16773, 16791]', 'Count=2', 'TDIF=2.0']]}

#	3) Merge Postings from each item in dictionary by Document ID

#Retrieve Posting Lists
def retrievePostingList(queryStr):
	
	#Open Document
	f1 = open("./INDEX.txt","r",errors="ignore")
	
	#Split query by space
	listQuery = queryStr.split()
	
	#Create a dictionary to hold postings of each word { word-str:Postings-list }
	dictPostings =  dict() 
	
	#Build dictPostings by finding the postings for each word 
	for word in listQuery:
		while True:
			line = f1.readline()
			if(parseLineFromWord(line) == word):
				dictPostings[word] = createPostingListFromStr(getStrPostingsFromLine(line))
	
	#Merge the dicPostings

	#Return the merge
	return

#Read word from line
def parseLineForWord(str1):
	""" Parse the word from the line """
	#EX: Word=aaainji:Postings=[['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']]
	#	 return aaainji
	#	 [5:] , read up to :
	indexColon = word.find(':')
	return str1[5:indexColon]

def getStrPostingsFromLine(str1):
	""" Get the List of Postings from Line """
	#Parse the posting from the line
	#EX: Word=aaainji:Postings=[['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']]
	#	 return [['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']]
	indexColon = str1.find('Postings=')
	return str1[indexColon + len("Postings="):]

def createPostingListFromStr(strPosting):
	""" Construct a Posting List from the line string """
	postingsList = list()
	while strPosting.find("DocID") != -1:
		tempDocList = []
		indexColon = strPosting.find("DocID")
		strPosting = strPosting[indexColon:]
		tempDocList.append(strPosting[0:strPosting.find("'")])
		
		indexColon = strPosting.find("Pos=")
		strPosting = strPosting[indexColon:]
		tempDocList.append(strPosting[0:strPosting.find("'")])
		
		indexColon = strPosting.find("Count=")
		strPosting = strPosting[indexColon:]
		tempDocList.append(strPosting[0:strPosting.find("'")])
		
		indexColon = strPosting.find("TDIF=")
		strPosting = strPosting[indexColon:]
		tempDocList.append(strPosting[0:strPosting.find("'")])
		
		postingsList.append(tempDocList)
	return postingsList

def main():
    #Type in query
    query = input("Enter your query: ")
    retrievePostingList(queryStr)

main()