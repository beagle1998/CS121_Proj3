
import os
from bs4 import BeautifulSoup
from collections import defaultdict
import re



print(os.path.isdir("C:\\Users\\tajun\\PycharmProjects\\ICS-121\\DevlopZip\\DEV"))
print(os.path.isfile("C:\\Users\\tajun\\PycharmProjects\\ICS-121\\DevlopZip\\DEV"))
print(os.path)

directory="C:\\Users\\tajun\\PycharmProjects\\ICS-121\\DevlopZip\\PracticeDEV"


for domain in os.scandir(directory):
    print(domain.path)
    for file in os.scandir(domain):
        scaped_text_dictionary=defaultdict(int)
        print(file.path)
        f1=open(file.path,"r")
        soup = BeautifulSoup(f1.read(), 'html.parser')
        ff=list(filter(None,(re.split((r"([\|\\][t|r|n])|[ ]"),soup.get_text()))))
        print(list(ff))
        f1.close()



#print(os.path.abspath("DevlopZip/DEV"))

#os.listdir("C:\\Users\\tajun\\PycharmProjects\\ICS-121\\DevlopZip\\DEV")
