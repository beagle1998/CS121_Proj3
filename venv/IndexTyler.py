import os
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import json
#asfasfasf

INDEX_DICT = {}
DOC_ID_DICT = {}
directory="C:\\Users\\tajun\\PycharmProjects\\ICS-121\\DevlopZip\\PracticeDEV"
doc_counter=0

#takes in a file name to tokenize and return a list of tokens
def Tokenizer(file):
            f1=open(file.path,"r")

            soup = BeautifulSoup(f1.read(), 'html.parser')
            f1.close()
            val=(json.loads(soup.get_text()))
            val2=str(val["content"])
            ff=list(filter(None,(re.split((r"[^\w0-9]+"),val2))))
            list2=[]
            for word in ff:
                if(re.match(r"[\w]+",word) and len(word)>1):
                    list2.append(word)
            #print(soup.get_text())
            return list2
#takes in file and token list, checks if dict has key=file _id, and updates accordingly, returns dict
def Index(ID,Tok_list):
    global INDEX_DICT
    for tok in Tok_list:
        if(tok in INDEX_DICT):
            INDEX_DICT[tok].add(ID)
        else:
            INDEX_DICT[tok]=set([ID])
    return


#map doc_id to doc url in a dict
def MAP_DOC_ID(domain,file):
    global doc_counter,DOC_ID_DICT
    place=str(file.path).split(directory)
    DOC_ID_DICT.update({doc_counter: place[1][1:]})
    doc_counter+=1
    return doc_counter-1

def main():

    for domain in os.scandir(directory):  # DEV FOlder
        print()
        for file in os.scandir(domain):  # url folder
            tok=Tokenizer(file)
            d_id=MAP_DOC_ID(domain,file)
            Index(d_id,tok)
    print(DOC_ID_DICT)
    print(INDEX_DICT)


    f1=open("INDEX","w+")
    for word,postings in INDEX_DICT.items():
        f1.write(str(word)+"::"+str(postings)+"\n")
    f1.close()
    f2=open("DOC_ID","w+")
    for word,postings in DOC_ID_DICT.items():
        f2.write(str(word)+"::"+str(postings)+"\n")
    f2.close()

main()


#print(os.path.abspath("DevlopZip/DEV"))

#os.listdir("C:\\Users\\tajun\\PycharmProjects\\ICS-121\\DevlopZip\\DEV")
