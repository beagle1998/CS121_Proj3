#USING THIS ONE NOW

import os
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import json
from nltk import PorterStemmer
from nltk.corpus import words
import math
import string
#asfasfasf

INDEX_DICT = {}
#DOC_ID_DICT = {}
directory="C:\\Users\\tajun\\PycharmProjects\\ICS-121\\DevlopZip\\PracticeDEV"
doc_counter=0
partial_counter=0
NumOfDocs=0
ps=PorterStemmer()
token_count=0
output_dict={}#where {filenum;(word,[list of postings]}
skip_count=0


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
        global skip_count
        word_pos=0
        f1=open(file.path,"r",errors="ignore")
        dict2 = {}
        soup = BeautifulSoup(f1.read(),"html.parser")
        f1.close()
        try:
            val=(json.loads(str(soup.text)))
            val2=str(val)

        except Exception as error:  # just skips file?
            print(str(error))
            print(file.path)
            skip_count+=1
            return dict2
        ff=list(filter(None,(re.split((r"[^a-zA-Z0-9]+"),val2))))
#          ff=filter(filter_stops,ff) # stop words             DO WE NEED THIS???

        for word in ff:
            word=(ps.stem(word)).lower()   #stemming here??
          #  try:
           #     word.decode("ascii")
      #      print(word) and word in words.words()  word.isalnum()  if(re.match(r"[a-zA-Z0-9]+",word)):
            if(is_ascii(word) and re.match(r"[a-zA-Z0-9]+",word)):
                if(str(word).isnumeric() and len(word)>4):
                   pass
                elif(word in dict2):
                    dict2[word].append(word_pos)
                    word_pos+=1
                else:
                    dict2[word]=[word_pos]
                    word_pos+=1

        return dict2

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

#puts items in tok_dict int INDEX_DICT for DOCID ID
def DOC_INDEX_DICT(ID,Tok_dict):
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
#WRITES FROM INDEX_DICT TO PINKEDX.txt
def write_partial_index():
    file="./PINDEX/PINDEX"+str(partial_counter)+".txt"
    f1 = open(file, "w+", encoding="utf-8")
    global INDEX_DICT
    # sorting index dict alpha
    for word, postings in sorted(INDEX_DICT.items()):
       # print((word))
        f1.write("Word=" + (word) + ":Postings=")
        f1.write("[")
        postings = sorted(postings, key=lambda v: v.tfidf, reverse=False)  # sorting postings of a word by tfidf
        for i in postings:
            # len(postings)=document frequency for a word
            # len(pos)=word freq in a doc
            i.tfidf = round((len(i.positions)), 2)
            f1.write(";DocID=" + str(i.docid) + "-Pos=" + str(i.positions) + "-Count=" + str(i.tfidf) + ";")
        f1.write("]\n")
    f1.close()
    INDEX_DICT={}

#inputs a readline from each of the partial indexes into output_list
    #output_list = {}  # where {filenum;(word,[list of postings]}, if you want to read from the file used for a word, just use the key of output_list which is f1, or f2, or fx
    #Word=conjunct::Postings=[{DocID=93,Pos=[200],TFIDF=0.5}{DocID=94,Pos=[409],TFIDF=0.5}] EXAMPLE OF THE READLINE OUTPUT
#open all partial index files, read a line from each, sort to find the lowest word, merge with base index, replace used line with a newline from its own file, and repeat.
def partial_index_read():
    global INDEX_DICT,partial_counter,output_dict,token_count
    #output_dict={file object:[file name,words and postings list]}
    #f1 = open("INDEX.txt", "w+", encoding="utf-8")#final INDEX IS INDEX.txt?BASE
    alpha=["0","1","2","3","4","5","6","7","8","9"]
    alpha.extend(list(string.ascii_lowercase))##opening 26 indexes, one for each letter case
    for k in alpha:
        global filealpha
        filealpha="./INDEX/INDEX"+str(k)+".txt"
        exec("f"+str(k)+"= open(filealpha, 'w+', encoding='utf-8')",globals(),globals())


    #reading from all files
    for i in range(partial_counter):#initializes outputlist per
        global file,file1
        file="./PINDEX/PINDEX"+str(i)+".txt"
        file1="fp"+str(i)
        exec(file1+"=open(file,"r")",globals(),globals())#making a new variable fx for each partial index where x is the PINDEX num
        exec("Index_line="+file1+".readline()",globals(),globals())
        Index_list=Index_line.split(':')#[word='',postings=['']
        Index_list[0]=Index_list[0][5:]
        Index_list[1]=Index_list[1][9:-1]
        output_dict[file1]=(file,Index_list[0],Index_list[1])

    while(len(output_dict)>=1):
        #print(output_dict["f0"])
        #print(file1)
        global lowest_word

        op1=list(output_dict.items())[0]
        lowest_file=[op1[0]]#list of
        lowest_word=[op1[1]]
        for j,k in output_dict.items():

            if(lowest_word[0][1]>k[1]):#searching for lowest word-list of tuple(file name,word,postings)
                lowest_word=[k]#resets the lists if a new lower word found.
                lowest_file=[j]

            if(lowest_word[0][1]==k[1]):
                if(lowest_word[0]==k):
                    pass
                else:
                    lowest_word.append(k)
                    lowest_file.append(j)
        #index_merge(lowest_word)#merge to base index
        token_count+=1

        #f1.write(str(index_merge(lowest_word))+"\n")
        #writing to each different index
        global merge_before
        merge_before=str(index_merge(lowest_word))+"\n"
        exec('f'+str(lowest_word[0][1][0])+'.write(merge_before)',globals(),globals())#+\n???

        #replacing lowest_word with next readline/word of its file.
        #CHECKING IF TO END A FILE READ OR NOT.
        for i in list(lowest_file):
            exec("partial_post="+i+".readline()",globals(),globals())
            if(partial_post==""):#if a partial index has reached its end close the file and delete its input into the output_dict
                exec(i + ".close()",globals(),globals())
                del output_dict[i]
            else:
                split1 = partial_post.split(':')  # [word='',postings=['']
                split1[0] = split1[0][5:]
                split1[1] = split1[1][9:-1]
                output_dict[i]=(i,split1[0],split1[1])

    for k in alpha:
        exec("f"+str(k)+".close()")
    #f1.close()

#takes in lowest word list, splits postings, merges, and returns a new line to write in f1.
def index_merge(low):
    # ;DocID = 84, Pos = [355], Count = 1.0;
    global token_count
    main_word="Word="+str(low[0][1])
    d3=[]
    list1=[]#list of postings[(i,o,p),(i,o,p)]
    list2=[]
    for i in low:#each represents a different partial index read from
        i=i[2]
        i=i.strip(r"[;]")#each diff document
        list1.append((i.split(";;")))#list of postings where each postings is a list of (docid,pos,count)

    num_p=len(list1)
    counterf=0
    #TIFIDF CALCULATING
    for i in list1:
        i=i[0]
        i=i.split('-')
        count=int(i[2][6:])#adjust count location? get word count
        i.append("TDIF="+str(round(((1+math.log(count,10))*(math.log(doc_counter/num_p,10))),2)))#(1+log(term count))*log(corpus size/number of docs with term in it)
        list1[counterf]=i
        counterf+=1
    list1=sorted(list1,key=lambda x:float(x[3][5:]),reverse=True)
    main_word+=":Postings="+str(list1)
    return main_word



def main():
    global INDEX_DICT,partial_counter,token_count
    fw=open("DOC_ID.txt","w+").close()
    for domain in os.scandir(directory):  # DEV FOlder
        print(domain)
        for file in os.scandir(domain):  # url folder
            tok=Tokenizer(file)
            d_id=MAP_DOC_ID(domain,file)   #ADDS DOC TO DOCID DICT, returns new DOC ID
            DOC_INDEX_DICT(d_id, tok)#fills DOC_INDEX with tokens for DOC ID
            if(d_id%1000==0):
                write_partial_index()#writes the current DOC_INDEX to file
                partial_counter+=1

    partial_index_read()#reads from all partial indexes
    # file_index()#merge and partial indexes
    print("Doc Count is ->"+str(doc_counter))
    print("Token Count is ->" + str(token_count))
    print("Number of skipped files="+str(skip_count))

main()