import xlrd
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.amazon
asin = db.asin

if asin.find_one({'flag':'zj'}) == None:
	asin.insert_one({'flag':'zj'})
else:
	pass

def read_excel(path):
    """
    读取exce中的数据 生成asin：sku字典
    一般都只读取第一行 ， 进行处理
    返回字典
    """
    asinSkuDict = {}
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    col0 = sheet.col_values(0)
    col0RealList = col0[3:-1]
    i = 0
    while i < len(col0RealList):
        asinSkuDict[col0RealList[i]] = ''
        i += 1
    return asinSkuDict


def update(asinToSku):
    """
    更新数据库
    无返回
    """
    asin.update({'flag': 'zj'}, {'$set': {'asinToSku': asinToSku}})



asinToSku = read_excel('new ad sku.xlsx')
print(asinToSku)
update(asinToSku)
