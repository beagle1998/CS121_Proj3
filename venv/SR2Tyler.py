# Search Retrivel Component
from nltk import PorterStemmer
import time
import linecache
from collections import defaultdict
import math

ps=PorterStemmer()
# Query 1
# Steps:


#	1) Type in Search:
#	"cristina lopes"

#	2) Get Postings Dictionary
#	cristina lopes
#	{"cristina": [['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']],
#   "lopes": [['DocID=2085', 'Pos=[16773, 16791]', 'Count=2', 'TDIF=2.0']]}

#	3) Merge Postings from each item in dictionary by Document ID

# Retrieve Posting Lists
def retrievePostingList(queryStr):
    # Open Document
    #f1 = open("./Index/INDEXa.txt", "r", errors="ignore")

    # Split query by space
    listQuery = queryStr.split()

    # Create a dictionary to hold postings of each word { word-str : Postings-list }
    dictPostings = dict()

    # Build dictPostings by finding the postings for each word
    lq = sorted(listQuery)
    wd = {}
    for i in range(len(lq)):
        wd[lq[i][0]]=[lq[i]]
        if((i+1)>=len(lq)):
            break;
        if(lq[i][0]==lq[i+1][0]):
            if(lq[i][0] in wd.keys()):
                wd[lq[i][0]].append(pq[i+1])
                i+=1
    for key,word_list in wd.items():
        f1 = open("./INDEX/INDEX" + key + ".txt", "r")
        for word in word_list:
            word = (ps.stem(word)).lower()  # stemming here??
            line = f1.readline()
            while line != "":
                if (parseLineFromWord(line) == word):
                    print(line)
                    dictPostings[word] = createPostingListFromStr(getStrPostingsFromLine(line))
                    break;
                line = f1.readline()
        f1.close()


    #Computing Cosine Scores #########
    dictCosineScores = defaultdict(int)
    dictLength = defaultdict(lambda:[0,0])
    dictQueryFreq = defaultdict(int)#first is W document, second is W of q,

    words=[]
    for i in queryStr.split():
        words.append((ps.stem(i)).lower())
        dictQueryFreq[i] += 1

    for word in words:
        #Calculat w(t,q)

        #Fetch Posting for word, loop postings list, calc score
        for posting in dictPostings[word]:
            #Posting Info
            tfidf = float(posting[3][5:])
            docid = int(posting[0][6:])
            count = int(posting[2][6:])
            #Add to score
            dictCosineScores[docid] += tfidf * ( tfidf / (1 + math.log(count,10)) * dictQueryFreq[word] )#* w(t, q)
            #Add to Length
            dictLength[docid][0] += (tfidf)**2
            dictLength[docid][1] += (( tfidf / (1 + math.log(count,10)))* dictQueryFreq[word])**2

    
    for d in dictCosineScores:
        dictCosineScores[d] = dictCosineScores[d] / (dictLength[d][0]**(1/2)+dictLength[d][1]**(1/2)) 

    #Return the dictionary of Cosine Scores
    return dictCosineScores

    # Merge the dicPostings, create {docId:[tfidf word1, 0 word2, tfidf word 3]
    """res = dict()  # {'docid':TDIF}
    
    for word, postings in dictPostings.items():
        #print(word,postings)
        if word in words:
            #print(word,"is in",words)
            for posting in postings:
                tdif = float(posting[3][5:])
                docid = int(posting[0][6:])

                if docid not in res:
                    #print(docid,"not in",res)
                    res[docid] = tdif
                    #print(res)
                else:
                    #print(docid,"is in",res)
                    res[docid] += tdif
            # print(res)

    print("results", res)"""
    # Return the merge
    #return res


def top5(res):#compares/get top5?
    res = sorted(res.items(), key=lambda kv: [kv[1], kv[0]], reverse=True)  # sorting
    print(res)
    docIdContainsWords = []  # all the doc ids
    for (docid, score) in res:
        docIdContainsWords.append(docid)
    docIdContainsWords = docIdContainsWords[:5]  # top 5
    print("top 5 ", docIdContainsWords)
    return docIdContainsWords


# Read word from line
def parseLineFromWord(str1):
    """ Parse the word from the line """
    # EX: Word=aaainji:Postings=[['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']]
    #	 return aaainji
    #	 [5:] , read up to :
    indexColon = str1.find(':')
    return str1[5:indexColon]


def getStrPostingsFromLine(str1):
    """ Get the List of Postings from Line """
    # Parse the posting from the line
    # EX: Word=aaainji:Postings=[['DocID=2085', 'Pos=[16772, 16791]', 'Count=2', 'TDIF=2.0']]
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

    # Type in query
    query = input("Enter your query: ")
    start_time = time.time()
    res = retrievePostingList(query)
    top5DocIds = top5(res)
    print("Run Time=" + str(round(time.time() - start_time, 3)))
    docs = []
    for l in top5DocIds:
        text = linecache.getline("DOC_ID.txt",l+1)
        indexUrl = len(str(l))+2
        url = text[indexUrl:-1]
        docs.append("DocID-"+str(l)+"="+url)
    print("top 5 docs=",docs)

main()
