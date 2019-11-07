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
            f1=open(file.path,"r")
            soup = BeautifulSoup(f1.read(), 'html.parser')
            f1.close()
            val=(json.loads(soup.get_text()))
            val2=str(val["content"])
            ff=list(filter(None,(re.split((r"[^\w0-9']+"),val2))))
 #          ff=filter(filter_stops,ff) # stop words             DO WE NEED THIS???
            dict2={}#maybe should be set
            for word in ff:
                word=(ps.stem(word)).lower()   #stemming here??
                if(re.match(r"[\w]+",word) and len(word)>1):
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
    global doc_counter,DOC_ID_DICT
    place=str(file.path).split(directory)
    DOC_ID_DICT.update({doc_counter: place[1][1:]})
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
    f1 = open("INDEX", "w+")
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
    f2 = open("DOC_ID", "w+")
    for word, postings in DOC_ID_DICT.items():
        f2.write(str(word) + "::" + str(postings) + "\n")
    f2.close()



def main():
    global INDEX_DICT
    for domain in os.scandir(directory):  # DEV FOlder
        for file in os.scandir(domain):  # url folder
            tok=Tokenizer(file)
            d_id=MAP_DOC_ID(domain,file)
            Index(d_id,tok)
    file_index()

main()
