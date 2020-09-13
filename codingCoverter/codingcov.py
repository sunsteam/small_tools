#-*- cofing: utf-8 -*-
import os
import sys
import cchardet

def getFileList(fileDir):
    fileList = []
    for root, dirs, files in os.walk(fileDir):
        fileList += [os.path.join(root, name) for name in files]
    return fileList


# 获取文件编码类型
def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return cchardet.detect(f.read())['encoding']


def resetCodingType(fileList, toCoding="UTF-8"):
    count = 0
    abort = 0
    success = 0
    failed = 0
    tmpNotClean = 0
    for f in fileList:
        f = f.replace("\\", "/")
        suffix = os.path.splitext(f)[1].lower()
        if suffix == ".cpp" or suffix == ".h":
            count += 1
            coding = get_encoding(f)
            # print ("suffix = %s, coding = %s" % (suffix, coding))
            if coding != toCoding.lower():
                # print ("iconv -f %s -t %s %s > \"%s.tmp\"" % (coding, toCoding, f, f))
                # print ("mv \"%s.tmp\" %s" % (f, f))
                
                if os.system("iconv -s -f %s -t %s %s > \"%s.tmp\"" % (coding, toCoding, f, f)) == 0:
                    if os.system("mv \"%s.tmp\" %s" % (f, f)) == 0:
                        success += 1
                    else:
                        tmpNotClean += 1
                        print ("file = %s.tmp need clean manually" % f)
                elif os.system("rm \"%s.tmp\"" % f) == 0:
                    abort += 1
                else:
                    failed += 1
                    print ("file = %s.tmp need clean manually" % f)

    print ("----------------------------------------------")
    print ("%d file count, %d completed, %d abort, %d needCleanTmp, %d failed" % (count, success, abort, tmpNotClean, failed))
    
if __name__ == "__main__":
    resetCodingType(getFileList("./target"), "UTF-8")


# iconv -f GBK -t UTF-8 原文件名 > 随便起个名
# -f是表示从什么编码，后面跟编码
# -t是表示转换到什么编码，后面跟编码
# >表示从哪个文件保存为哪个文件
# iconv --list 显示支持的所有编码
# find *.txt -exec sh -c "iconv -f GBK -t UTF-8 {} > {}.tmp"
