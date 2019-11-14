
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
	
	print("This is the query you are searching: ", listQuery)

	#Create a dictionary to hold postings of each word { word-str:Postings-list }
	dictPostings =  dict() 
	
	#Build dictPostings by finding the postings for each word 
	
	line = f1.readline()
	while line != EOFError:
		if(parseLineFromWord(line) in listQuery):
			word = parseLineFromWord(line)
			listQuery.pop(word)
			print("Found word: " + str(word))
			dictPostings[word] = createPostingListFromStr(getStrPostingsFromLine(line))
			
		line = f1.readline()
	
	#Merge the dicPostings
	res = dict() #{'docid':TDIF}
	words = queryStr.split()
	for word,postings in dictPostings.items():
		#print(word,postings)
		if word in words:
		#print(word,"is in",words)
			for posting in postings:
				tdif = float(posting[3][5:])
				docid = int(posting[0][6:])
				if docid not in res:
				#print(docid,"not in",res)
					res[docid]=tdif
				#print(res)
				else:
				#print(docid,"is in",res)
					res[docid]+=tdif
				#print(res)

	print("results",res)
	#Return the merge
	return res
def top5(res):
	res = sorted(res.items(),key=lambda kv:[kv[1],kv[0]],reverse=True) #sorting 
	print(res)
	docIdContainsWords=[] #all the doc ids
	for (docid,score) in res:
		docIdContainsWords.append(docid)
	docIdContainsWords = docIdContainsWords[:5] #top 5
	print("top 5 ",docIdContainsWords)
	return docIdContainsWords
#Read word from line
def parseLineFromWord(str1):
	""" Parse the word from the line """
	#EX: Word=aaainji:Postings=[['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']]
	#	 return aaainji
	#	 [5:] , read up to :
	indexColon = str1.find(':')
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
    res = retrievePostingList(query)
    top5DocIds = top5(res) 

main()
