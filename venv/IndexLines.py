
import os
directory = "./INDEX"

fLen = open("IndexLines.txt","w+")

for file in os.scandir(directory):
	f = open(file,"r")
	fLen.write( str( len(f.readlines() ) ) + "\n")