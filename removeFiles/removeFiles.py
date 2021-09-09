# -*- cofing: utf-8 -*-
import os
import sys
import re


def getFileList(root, files, targetSuffixs, fileNames):
    fileList = ""
    for fullName in files:
        part = os.path.splitext(fullName)
        suffix = part[1].lower()
        name = part[0].lower()
        if suffix in targetSuffixs or name in fileNames:
            fileList += "f----{}\n".format(os.path.join(root, fullName))
    return fileList


def getDirList(root, dirs, dirNames):
    dirList = ""
    for name in dirs:
        if name in dirNames:
            dirList += "d----{}\n".format(os.path.join(root, name))
    return dirList


def readConfig(configFile, suffixs, fileNames, dirNames):
    if os.path.exists(configFile) and os.path.isfile(configFile):
        config = open(configFile, "r", encoding="UTF-8")
        lines = config.readlines()
        flag = ""
        for line in lines:
            line = line.replace("\n", "")
            if line.startswith("---"):
                flag = re.search("---(.+)---", line).group(1)
                continue

            if flag == "suffix":
                suffixs += [".{}".format(line)]
            elif flag == "fileName":
                fileNames += [line]
            elif flag == "dirName":
                dirNames += [line]
    else:
        config = open(configFile, "x", encoding="UTF-8")
    config.close()


def checkTargets(dirPath):
    suffixs = []
    fileNames = []
    dirNames = []
    readConfig("config.ini", suffixs, fileNames, dirNames)
    fileList = ""
    dirList = ""
    record = open("list.txt", "w+", encoding="UTF-8")

    for root, dirs, files in os.walk(dirPath, followlinks=True):
        fileList += getFileList(root, files, suffixs, fileNames)
        dirList += getDirList(root, dirs, dirNames)
    # print(fileList+dirList)
    record.write(fileList + dirList)
    record.close()

    print("done")
    os.system("start notepad.exe list.txt")


def removeDirs(dirPath):
    if os.path.exists(dirPath):
        for root, dirs, files in os.walk(dirPath, followlinks=True, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(dirPath)
        print("removed dir %s" % dirPath)


def removeTargets():
    if os.path.exists("list.txt") and os.path.isfile("list.txt"):
        f = open("list.txt", "r", encoding="UTF-8")
        lines = f.readlines()
        f.close()

        for line in lines:
            flag = line[0]
            line = line[5:].replace("\n", "")

            if flag == "f" and os.path.exists(line):
                os.remove(line)
                print("removed file %s" % line)
            elif flag == "d":
                removeDirs(line)

        print("remove done")


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 3 and argv[1] == "-c":
        checkTargets(argv[2])
    elif len(argv) == 2 and argv[1] == "-d":
        removeTargets()
    else:
        print(
            "python cleaner.py <option> <path>\n -c check targets, f---- means file, d---- means directory\n -d delete targets in list.txt"
        )
