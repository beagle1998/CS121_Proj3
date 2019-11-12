import os
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import json
from nltk import PorterStemmer
from nltk.corpus import words
#asfasfasf

INDEX_DICT = {}
#DOC_ID_DICT = {}
directory="C:\\Users\\marce\\Documents\\cs 121\\assignment3\\PracticeDEV"
doc_counter=0
partial_counter=0
NumOfDocs=0
ps=PorterStemmer()
token_count=0



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
        f1=open(file.path,"r",errors="ignore")

        soup = BeautifulSoup(f1.read(), 'html.parser')
        f1.close()
        val=(json.loads(soup.get_text()))
        val2=str(val["content"])
        ff=list(filter(None,(re.split((r"[^\w0-9']+"),val2))))
#          ff=filter(filter_stops,ff) # stop words             DO WE NEED THIS???
        dict2={}#maybe should be set
        for word in ff:  
            word=(ps.stem(word)).lower()   #stemming here??
            print(word)
            '''
          #  try:
           #     word.decode("ascii")
      #      print(word) and word in words.words()
	        '''
	        #print(word)
            if(word.isalnum()):
                if(word in dict2):
                    dict2[word].append(word_pos)
                    word_pos+=1
                else:
                    dict2[word]=[word_pos]
                    word_pos+=1
         #   except:
            #    pass

        return dict2
#takes in file and token list, checks if dict has key=file _id, and updates accordingly, returns dict
#index dict holds keys for word, but sets containg the id and a list of positons
def Partial_Index(ID,Tok_dict):
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
    file="PINDEX"+str(partial_counter)+".txt"
    f1 = open(file, "w+", encoding="utf-8")
    global INDEX_DICT
    # sorting index dict alpha
    for word, postings in sorted(INDEX_DICT.items()):
        #print((word))
        f1.write("Word=" + (word) + "::Postings=")
        f1.write("[")
        postings = sorted(postings, key=lambda v: v.tfidf, reverse=False)  # sorting postings of a word by tfidf
        for i in postings:
            # len(postings)=document frequency for a word
            # len(pos)=word freq in a doc
            i.tfidf = round((len(i.positions) / len(postings)), 2)
            f1.write("{DocID=" + str(i.docid) + ",Pos=" + str(i.positions) + ",TFIDF=" + str(i.tfidf) + "}")
        f1.write("]\n")
    f1.close()
    INDEX_DICT={}

def partial_index_write_merge():
    f1 = open("INDEX.txt", "w+")
    global INDEX_DICT
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
    INDEX_DICT = {}

def main():
    #print("hasda")
    global INDEX_DICT,partial_counter,token_count
    fw=open("DOC_ID.txt","w+").close()
    for domain in os.scandir(directory):  # DEV FOlder
        print(domain)
        for file in os.scandir(domain):  # url folder
            tok=Tokenizer(file)
            d_id=MAP_DOC_ID(domain,file)
            Partial_Index(d_id, tok)
            if(d_id%100==0):
                file_index()
                partial_counter+=1

    file_index()#merge and partial indexes
    print("Doc Count is ->"+str(doc_counter))

main()
