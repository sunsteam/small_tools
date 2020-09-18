# -*- cofing: utf-8 -*-
import os
import sys

def revise(filePath):
    inputF = open(filePath,"r",encoding="UTF-8")
    lines = inputF.readlines()
    inputF.close()
    outStr = ""
    for line in lines:
        line = line.replace("\n","<br/>\n")
        outStr += line
    with outputF = open("revised.html","w",encoding="UTF-8")
        outputF.write(outStr)
    


    
if __name__ == "__main__":
    revise(sys.argv[1])
