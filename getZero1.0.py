from getPage import GetPage
from searchZeroAndReturn import SearchAndReturn
from pymongo import MongoClient
import time
from getWeChatMes import writefile

# 连接数据库
conn = MongoClient('localhost', 27017)
db = conn.amazon
asinDB = db.asin

def getIsZero(asin):
    """
    通过asin 获取url
    判断确认库存为零的asin
    通过asinDict来获取sku
    写入文件isLack.txt
    """
    url = 'https://www.amazon.com/dp/%s' % asin
    getRealPage = GetPage(url)
    driver = getRealPage.open_chrome()

    try:
        getEachZero = SearchAndReturn(driver, asin)
        if getEachZero.check_list_or_2x2() == 0:  # 判断能否选择size
            if getEachZero.check_urls_list():
                print('asin %s 缺货1' % asin)
                return asin
            else:
                print('asin %s 不缺货1' % asin)
        else:
            if getEachZero.check_urls_2x2():
                print('asin %s 缺货2' % asin)
                return asin
            else:
                print('asin %s 不缺货2' % asin)
        return ''
    except Exception as e:
        print(e, asin)
    finally:
        getRealPage.close_chrome(driver)


if __name__ == '__main__':
    realList = [[], []]
    i = -1
    while True:
        """
        连续两次的结果进行对比
        如果两次都有， 则进行输出
        数据校对 两次都出错的可能性较低
        """
        startTime = time.time()
        asinDict = asinDB.find_one()['asinToSku']
        asinList = [i for i in asinDict]
        # asinList = ['B07CPLDJB2']
        zeroList = []
        for asin in asinList:
            try:
                zeroAsin = getIsZero(asin)
                if zeroAsin != '':
                    zeroList.append(zeroAsin)
            except:
                pass

        print('"""\n %s \n"""' % zeroList)
        zeroList = list(set(zeroList))

        if i == -1:
            realList[0] = zeroList
        else:
            realList[1] = zeroList

        i = -i
        outputList = [i for i in realList[0] for j in realList[1] if i == j]
        writefile('isLack.txt', outputList)

        endTime = time.time()
        untilTime = endTime - startTime
        print(' 运行总时长 %s\n realList 为%s' % (untilTime, realList))
