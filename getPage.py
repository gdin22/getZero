#！/user/bin/env python
# _*_ coding:utf-8 _*_

from selenium import webdriver
# from pymongo import MongoClient
# import random


class GetPage:
    def __init__(self, url):
        """
        self.conn = MongoClient('localhost', 27017)
        self.userAgent = self.conn.self.userAgent
        self.userList = self.userAgent.find_one()['userAgent']
        self.user = random.choice(self.userList)
        """
        self.url = url

    def noDesk(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
        return  chrome_options

    def noPicture(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options

    def open_chrome(self):  # 打开浏览器
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(self.url)
        return driver

    @staticmethod
    def close_chrome(driver):  # 静态方法关闭浏览器
        driver.close()
        driver.quit()
