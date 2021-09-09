# -*- cofing: utf-8 -*-
import os
import io
import pandas as pd
from pandas.core.frame import DataFrame

templatePath = r"D:/small_tools/py_tools/pandas/template.csv"
lotName = None
zeroStr = "0.00E+00"


def reformat(filePath) -> bool:
    assert isinstance(filePath, str)
    if filePath[-3:].lower() != "csv":
        return False
    # 处理文件名
    tempName = os.path.split(filePath)[-1][:-4].replace("_", "-")
    productName = tempName.split("-")[0]
    global lotName
    lotName = tempName.split("-")[1]
    waferName = "0" + tempName.split("-")[2]
    tempName = "-".join([productName, lotName, waferName])
    # 从源数据抽取需要的内容
    inputF = open(filePath, "r", encoding="UTF-8")
    lines = inputF.readlines()
    inputF.close()

    with io.StringIO() as stream:
        headList = None
        numberList = None
        # 合并14和31行数据
        for i, lineStr in enumerate(lines):
            if i == 14:
                headList = lineStr.split(",")
            if i == 31:
                numberList = lineStr.split(",")
                for j, item in enumerate(headList):
                    headList[j] = item + "_" + numberList[j]
                lineStr = ",".join(headList)
                lineStr = lineStr[:-2]
                stream.write(lineStr)
            if i > 31:
                stream.write(lineStr)
        update(stream, tempName)
    return True


def update(stream: io.StringIO, tempName: str):
    # 创建保存目录
    dirPath = os.path.join(r"C:/BYD/DATA", lotName)
    os.makedirs(dirPath, exist_ok=True)
    tempPath = os.path.join(dirPath, tempName)
    # 转换数据为csv
    stream.seek(0)
    tempData = pd.read_csv(stream, na_values=["Untested"], dtype="str")
    assert isinstance(tempData, DataFrame)
    # 删除多余列
    headers = list(tempData.columns)
    headers[0] = "Item Name"
    headers[1] = "BIN"
    tempData.columns = headers
    tempData = tempData.loc[:, ~tempData.columns.str.contains("^_|^Unnamed|^SAME")]
    tempData.drop(
        columns=["X-AXIS_T1", "Y-AXIS_T2", "PASS#_T3", "DEF_T34"], inplace=True
    )
    # 增加额外列
    tempData.insert(10, "DELAY", zeroStr)
    tempData.insert(19, "SHORT", zeroStr)
    tempData.insert(len(tempData.columns) - 1, "SHORT ", zeroStr)

    # 列名编号
    headers = list(tempData.columns)
    for i, header in enumerate(headers):
        if i > 1:
            headers[i] = "{} {}".format(i - 1, header)
    tempData.columns = headers

    tempData["1 CONT_T4"] = zeroStr
    # tempData.to_csv(tempPath + "-temp.csv")

    # 读取，修改模板
    df = pd.read_csv(templatePath, header=None)
    assert isinstance(df, DataFrame)

    df.iat[2, 2] = tempPath + ".njdf"
    df.iat[5, 2] = lotName
    for i in range(21, 21 + len(tempData.index)):
        df.loc[i] = ''
    df.iloc[21:, :] = tempData.iloc[0:, :]

    df.to_csv(tempPath + ".csv", index=False, header=False)


reformat(r'D:/workfile/上海先进/6M20214数据转换/data/6M20214-712016/6M20214-712016_19.CSV')

# if __name__ == "__main__":
#     format(sys.argv[1])
