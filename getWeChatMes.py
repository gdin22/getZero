import itchat
from itchat.content import *
import time
import threading
from pymongo import MongoClient
import os

"""
连接mongodb数据库
修改数据库配置
"""
conn = MongoClient('localhost', 27017)
db = conn.amazon
asin = db.asin
asinDict = asin.find_one({'flag': 'zj'})['asinToSku']


@itchat.msg_register(TEXT)
def simple_reply(msg):
    """
    监听收到的信息
    进行处理 约定好 如果第一个字符为‘+’ 则对asin和sku进行 增加操作
    如果第一个字符为‘-’ 则对asin进行 删除操作
    """
    text = msg['Text']
    addOrCut = text.split(' ')[0]
    asinlist = text.split(' ')[1:]

    users = itchat.search_friends('凯哥')  # 输入信息获取人
    userName = users[0]['UserName']

    if addOrCut == '+':
        for oneAsin in asinlist:
            asinDict[oneAsin] = ''
        itchat.send('更新成功', userName)
    elif addOrCut == '-':  # 判断此asin 是否在数据库里
        for oneAsin in asinlist:
            if oneAsin in asinDict:
                asinDict.pop(oneAsin)
        itchat.send('更新成功', userName)
    elif addOrCut == 'list':
        asinMessage = ''.join([i for i in asinDict])
        itchat.send(asinMessage, userName)
    else:
        itchat.send('出现错误', userName)
    asin.update({'flag': 'zj'}, {'$set': {'asinToSku': asinDict}})


def returnText():
    """
    每半个小时对文本内容进行发送
    """
    while True:
        print('begin')
        users = itchat.search_friends('凯哥')  # 输入信息获取人
        userName = users[0]['UserName']
        message = readfile('isLack.txt')

        """
            itchat.send(str(time.time()), 'filehelper')
        """
        if len(message.strip()) != 0:
            itchat.send(message, userName)
        else:
            pass
        # 需要删掉文件 避免读两次
        try:
            os.remove('isLack.txt')
        except Exception as e:
            print(' 没有文件时抛出错误 正常\n错误为:%s' % e)

        time.sleep(60*60)


def writefile(file, asinlist):
    with open(file, 'w+') as f:
        for mes in asinlist:
            if mes != None and mes in asinDict.keys():
                    f.write(mes + ' ')


def readfile(file):
    try:
        with open(file, 'r') as f:
            text = f.read()
        return text
    except Exception as e:
        print('没有文件时出错 程序正常\n错误为:%s' % e)
        return ''


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    t1 = threading.Thread(target=returnText, args=())  # 开启线程
    t1.start()
    itchat.run()

