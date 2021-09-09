# -*- cofing: utf-8 -*-
import os
import sys


def revise(filePath):
    inputF = open(filePath, "r", encoding="UTF-8")
    text = inputF.read()
    inputF.close()
    with open("revised", "w", encoding="UTF-8") as outputF:
        outputF.write(reviseText(text))


def reviseText(text: str) -> str:
    outStr = ""
    start = 0
    found = 0
    while True:
        found = text.find("\n", start)
        if found == -1:
            outStr += text[start:]
            break
        outStr += text[start:found]
        start = found + 1
        if text[found + 1 : found + 4] != "167":
            outStr += " "
        else:
            outStr += "\n"

    return outStr


if __name__ == "__main__":
    revise(sys.argv[1])
