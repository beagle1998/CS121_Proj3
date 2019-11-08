import os
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import json
from nltk import PorterStemmer
#asfasfasf

INDEX_DICT = {}
DOC_ID_DICT = {}
directory="C:\\Users\\tajun\\PycharmProjects\\ICS-121\\DevlopZip\\PracticeDEV"
doc_counter=0
NumOfDocs=0
ps=PorterStemmer()



class Postings:#each doc id is a posting?
    def __init__(self, docid,positions):
        self.docid = docid
        self.positions = positions
        self.tfidf=0  # use freq counts for now
     #   self.fields = fields





#takes in a file name to tokenize and return a list of tokens//should return a list of lists? where first element is tok, second is count, third is and so on.
#1:tok,2:count,3:list of pos?
#tokenizer returns a dict of words as keys and word positions as values in a list form
def Tokenizer(file):
            word_pos=0
            dict2 = {}
            f1=open(file.path,"r")
            soup = BeautifulSoup(f1.read(), 'html.parser')
            f1.close()
            try:
            #al=(soup.get_text())
                val=json.loads(soup.get_text())
                val=str(val["content"])
            except ValueError:
                return dict2
            #print(val)
            ff=list(filter(None,(re.split((r"[^\w']+"),val))))
 #          ff=filter(filter_stops,ff) # stop words             DO WE NEED THIS???
            #maybe should be set
            for word in ff:
               # print(word)
                word=(ps.stem(word)).lower()   #stemming here??
                if(word.isalnum()):
                    print(word)
                    if(word in dict2):
                        dict2[word].append(word_pos)
                        word_pos+=1
                    else:
                        dict2[word]=[word_pos]
                        word_pos+=1

            return dict2
#takes in file and token list, checks if dict has key=file _id, and updates accordingly, returns dict
#index dict holds keys for word, but sets containg the id and a list of positons
def Index(ID,Tok_dict):
    global INDEX_DICT
    for tok,pos in Tok_dict.items():#tok dict pos is a list there should be no repeates?
            if(tok not in INDEX_DICT):
                INDEX_DICT[tok]=[Postings(ID,pos)]#list of Postings???
            else:
                INDEX_DICT[tok].append(Postings(ID,pos))
    return

#map doc_id to doc url in a dict
def MAP_DOC_ID(domain,file):
    global doc_counter
    place=str(file.path).split(directory)
    f2 = open("DOC_ID.txt", "a+")
    f2.write(str(doc_counter) + "::" + str(place[1][1:]) + "\n")
    f2.close()
    doc_counter+=1
    return doc_counter-1

def filter_stops(f):
    f2 = open("stop_words.txt", "r")
    stop_list = f2.read().split('\n')
    f2.close()
    if f.lower() in stop_list:#only takes out the non stop words
        return False
    else:
        return True

def file_index():
    f1 = open("INDEX.txt", "w+")
    # sorting index dict alpha
    for word, postings in sorted(INDEX_DICT.items()):
        f1.write("Word=" + str(word) + "::Postings=")
        f1.write("[")
        postings = sorted(postings, key=lambda v: v.tfidf, reverse=False)  # sorting postings of a word by tfidf
        for i in postings:
            # len(postings)=document frequency for a word
            # len(pos)=word freq in a doc
            i.tfidf = round((len(i.positions) / len(postings)), 2)
            f1.write("{DocID=" + str(i.docid) + ",Pos=" + str(i.positions) + ",TFIDF=" + str(i.tfidf) + "}")
        f1.write("]\n")
    f1.close()



def main():
    global INDEX_DICT
    fw=open("DOC_ID.txt","w+").close()
    for domain in os.scandir(directory):  # DEV FOlder
        print(domain)
        for file in os.scandir(domain):  # url folder
            print(file)
            tok=Tokenizer(file)
            d_id=MAP_DOC_ID(domain,file)
            Index(d_id,tok)

    file_index()#merge and partial indexes
    print("Doc Count is ->"+str(doc_counter))
    print("Token Count is ->"+str(len(INDEX_DICT)))

main()
