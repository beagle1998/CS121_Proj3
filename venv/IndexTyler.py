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
directory="C:\\Users\\tajun\\PycharmProjects\\ICS-121\\DevlopZip\\PracticeDEV"
doc_counter=0
partial_counter=0
NumOfDocs=0
ps=PorterStemmer()
token_count=0
output_dict={}#where {filenum;(word,[list of postings]}



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
        try:
            val=(json.loads(soup.get_text()))
            val2=str(val["content"])
        except TypeError:#just skips file?
            pass

        ff=list(filter(None,(re.split((r"[^\w0-9]+"),val2))))
#          ff=filter(filter_stops,ff) # stop words             DO WE NEED THIS???
        dict2={}#maybe should be set
        for word in ff:
            word=(ps.stem(word)).lower()   #stemming here??
          #  try:
           #     word.decode("ascii")
      #      print(word) and word in words.words()  word.isalnum()  if(re.match(r"[a-zA-Z0-9]+",word)):
            if(is_ascii(word) and re.match(r"[a-zA-Z0-9]+",word)):
                if(word in dict2):
                    dict2[word].append(word_pos)
                    word_pos+=1
                else:
                    dict2[word]=[word_pos]
                    word_pos+=1
         #   except:
            #    pass

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
def write_index():
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
            i.tfidf = round((len(i.positions) / len(postings)), 2)
            f1.write("{DocID=" + str(i.docid) + ",Pos=" + str(i.positions) + ",TFIDF=" + str(i.tfidf) + "}")
        f1.write("]\n")
    f1.close()
    INDEX_DICT={}

#inputs a readline from each of the partial indexes into output_list
    #output_list = {}  # where {filenum;(word,[list of postings]}, if you want to read from the file used for a word, just use the key of output_list which is f1, or f2, or fx
    #Word=conjunct::Postings=[{DocID=93,Pos=[200],TFIDF=0.5}{DocID=94,Pos=[409],TFIDF=0.5}] EXAMPLE OF THE READLINE OUTPUT
#open all partial index files, read a line from each, sort to find the lowest word, merge with base index, replace used line with a newline from its own file, and repeat.
def partial_index_read():
    global INDEX_DICT,partial_counter,output_dict

    #output_dict={file object:[file name,words and postings list]}
    f1 = open("INDEX.txt", "w+")#final INDEX IS INDEX.txt?BASE
    #reading from all files
    for i in range(partial_counter):#initializes outputlist per
        global file,file1
        file="./PINDEX/PINDEX"+str(i)+".txt"
        file1="fp"+str(i)

        exec(file1+"=open(file,"r")",globals(),globals())#making a new variable fx for each partial index where x is the PINDEX num

        #print(fp0.readline())

        exec("Index_line="+file1+".readline()",globals(),globals())

        Index_list=Index_line.split(':')#[word='',postings=['']
        Index_list[0]=Index_list[0][5:]
        Index_list[1]=Index_list[1][9:-1]
        output_dict[file1]=(file,Index_list[0],Index_list[1])
          #exec("output_dict["+file1+"]=("file+","+#inputting a readline from each partial index into output list.


    #output_sorted=sorted(output_dict,key=lambda x,y:y[0])#sorts the output dict by the dict.values[0] which is the WORD    and puts it into a list? is output_dict affected or the same still?
    #index_merge(output_sorted[0])
    while(len(output_dict)>=1):
        #print(output_dict["f0"])
        #print(file1)

        op1=list(output_dict.items())[0]
        lowest_file=[op1[0]]#list of
        lowest_word=[op1[1]]
        for j,k in output_dict.items():

            if(lowest_word[0][1]>k[1]):#searching for lowest word
                lowest_word=[k]#resets the lists if a new lower word found.
                lowest_file=[j]

            if(lowest_word[0][1]==k[1]):
                if(lowest_word[0]==k):
                    pass
                else:
                    lowest_word.append(k)
                    lowest_file.append(j)
        #index_merge(lowest_word)#merge to base index

        f1.write(str(lowest_word[0])+"\n")


        #replacing lowest_word with next readline/word of its file.
        for i in list(lowest_file):
            exec("partial_post="+i+".readline()",globals(),globals())
            if(partial_post==""):#if a partial index has reached its end close the file and delete its input into the output_dict

                exec(i + ".close()",globals(),globals())
                del output_dict[i]
            else:
                output_dict[i]=partial_post
    f1.close()

#d_p is [0]=word,[1]=list of postings
def index_merge(d_p):
   pass



def TOKEN_COUNT():
    pass
def main():
    global INDEX_DICT,partial_counter,token_count
    fw=open("DOC_ID.txt","w+").close()
    for domain in os.scandir(directory):  # DEV FOlder
        print(domain)
        for file in os.scandir(domain):  # url folder
            tok=Tokenizer(file)
            d_id=MAP_DOC_ID(domain,file)   #ADDS DOC TO DOCID DICT, returns new DOC ID
            DOC_INDEX_DICT(d_id, tok)#fills DOC_INDEX with tokens for DOC ID
            if(d_id%100==0):
                write_index()#writes the current DOC_INDEX to file
                partial_counter+=1
    partial_index_read()#reads from all partial indexes

    # file_index()#merge and partial indexes
    print("Doc Count is ->"+str(doc_counter))

main()