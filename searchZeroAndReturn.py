import time
import random


class SearchAndReturn:
    """
    获取打开的driver
    获取库存为零的size和color
    库存为零的一句 透明度不同 class_name不同
    """
    def __init__(self, driver, asin):
        self.driver = driver
        self.asin = asin

    def get_page_zero(self):
        zero_size_color = {}
        if self.check_list_or_2x2():
            """
            没出错即为有size选项
            """
            self.driver.find_element_by_id('dropdown_selected_size_name').click()
            size_count = len(self.driver.find_elements_by_class_name('a-dropdown-item'))
            for size_num in range(size_count-1):
                get_id = 'size_name_%s' % str(size_num)
                size_color = self.get_real_color_size(get_id)
                zero_size_color.update(size_color)
                self.driver.find_element_by_id('dropdown_selected_size_name').click()
                time.sleep(random.randint(1, 5))
            return zero_size_color
        else:
            """
            出错即为没有size选项
            """
            zero_size_color = {'None': self.get_zero_element_list()}
            return zero_size_color

    def get_real_color_size(self, get_id):
        """
        get_id 为当前size的id
        选择 然后查看size 得到库存为零的颜色
        返回一个size:color_size字典
        """
        self.driver.find_element_by_id(get_id).click()
        size = self.driver.find_element_by_class_name('a-dropdown-prompt').text
        color_list = self.get_zero_element_list()
        return {size: color_list}

    def get_zero_element_list(self):
        """
        选好size后 库存为零的 将其颜色 添加到color_list
        """
        colors_driver = self.driver.find_elements_by_class_name('swatchUnavailable')
        color_list = []
        for each_color_driver in colors_driver:
            color_list.append(each_color_driver.get_attribute('title').split(' select ')[-1].strip())
        return color_list

    def check_urls_2x2(self):
        # print('in check_urls_2x2')
        """
        在得到有asin的driver后 只能得到颜色 不能得到大小
        返回flag flag为True时 库存为零 flag 为False时 库存不为零
        用于2*2 即可选择size
        选择后对链接进行判断即可 如果能匹配到其链接则为有库存
        """
        flag = True
        size_count = len(self.driver.find_elements_by_class_name('a-dropdown-item'))
        for size_num in range(size_count - 1):
            get_id = 'size_name_%s' % str(size_num)
            print('get_id %s' % get_id)
            if self.driver.find_element_by_id(get_id).get_attribute('class').find('dropdownAvailable') != -1:
                self.driver.find_element_by_id(get_id).click()
                time.sleep(5)
                current_url = self.driver.current_url
                print(current_url)
                if current_url.find(self.asin) != -1:
                    flag = False
                    break
                self.driver.find_element_by_id('dropdown_selected_size_name').click()
            else:
                pass
        return flag

    def check_urls_list(self):
        # print('in check_urls_list')
        """
        在列表中选择 能够选中的和已被选中的 进行抓取asin 再对本身asin进行比对 如果有相同的则还有库存 否则相反
        用于列表 即为不能选择颜色
        返回flag flag为True时 库存为零 flag 为False时 库存不为零
        """
        flag = True
        aslist = []
        for element in self.driver.find_elements_by_class_name('swatchAvailable') + self.driver.find_elements_by_class_name('swatchSelect'):
            print(element.get_attribute('data-defaultasin'))
            aslist.append(element.get_attribute('data-defaultasin'))

        try:
            aslist.index(self.asin)
            flag = False
        except:
            pass
        return flag

    def check_list_or_2x2(self):
        """
        判断有无size选项
        """
        list_or_2x2 = 0
        try:
            self.driver.find_element_by_id('dropdown_selected_size_name').click()  # 会先把size点击开来
            list_or_2x2 = 1
        except Exception as e:
            print(e, self.asin)
            pass
        return list_or_2x2
