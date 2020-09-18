# -*- cofing: utf-8 -*-
import os
import sys
import cchardet
import codecs

def getFileList(fileDir):
    fileList = []
    for root, dirs, files in os.walk(fileDir):
        fileList += [os.path.join(root, name) for name in files]
    return fileList


def getFileContent(filePath):
    with codecs.open(filePath, 'rb') as f:
        return f.read()


def addUtf8Bom(filePath):
    data = getFileContent(filePath)
    if data[:3] == codecs.BOM_UTF8:
        return 666
    
    with open("{}.tmp".format(filePath), "wb") as f:
        f.write(codecs.BOM_UTF8)
        f.write(data)
    return 0

def removeUtf8Bom(filePath):
    data = getFileContent(filePath)
    if data[:3] == codecs.BOM_UTF8:
        return 666

    data = data[3:]
    with open("{}.tmp".format(filePath), "wb") as f:
        f.write(data)
    return 0


def convert2Utf8(fileList, withBom = False):
    count = 0
    abort = 0
    success = 0
    failed = 0
    toCoding = "utf-8"
    for f in fileList:
        f = f.replace("\\", "/")
        suffix = os.path.splitext(f)[1].lower()
        if suffix == ".cpp" or suffix == ".h":
            count += 1
            coding = cchardet.detect(getFileContent(f))['encoding'].lower()
            name = os.path.splitext(f)[0].lower()
            result = 666
            
            if not coding.startswith(toCoding) and coding != "ascii":
                #print ("file = %s, coding = %s" % (f,coding))
                if coding == "windows-1252":
                    coding = "gb2312"
                result = os.system("iconv -f %s -t %s \"%s\" > \"%s.tmp\"" % (coding, toCoding, f, f))
            elif toCoding == "utf-8":
                result = addUtf8Bom(f) if withBom else removeUtf8Bom(f)
            else: 
                abort += 1
                continue

            if result == 0:
                success += 1
            elif result == 666:
                abort += 1
            else:
                failed += 1
                print ("file = %s, coding = %s, convert failed" % (f, coding))

            if os.path.exists("{}.tmp".format(f)) and os.system("mv \"%s.tmp\" \"%s\"" % (f, f)) != 0:
                    print ("file = %s.tmp need clean manually" % f)

    print ("----------------------------------------------")
    print ("%d file count, %d success, %d abort, %d failed" % (count, success, abort, failed))


    
if __name__ == "__main__":
    convert2Utf8(getFileList("./target"), True)


# iconv -f GBK -t UTF-8 原文件名 > 随便起个名
# -f是表示从什么编码，后面跟编码
# -t是表示转换到什么编码，后面跟编码
# >表示从哪个文件保存为哪个文件
# iconv --list 显示支持的所有编码
# find *.txt -exec sh -c "iconv -f GBK -t UTF-8 {} > {}.tmp"
