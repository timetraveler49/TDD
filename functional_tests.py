from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # xx听说有一个在线待办事项的应用
        # 他去看了这个应用的首页
        self.browser.get('http://localhost:8000')

        # 他注意到网页里有“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # 应用有一个输入待办事项的文本输入框
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )


        # 他在文本输入框输入了“Buy flowers”
        inputbox.send_keys('Buy flowers')
        # 他按下回车后，页面更新
        # 待办事项表格显示“1:Buy flowers”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Buy flowers', [row.text for row in rows])
        # 页面中又显示了一个文本输入框，可以输入其他待办事项
        # 输入"Send a gift to Lisa"
        self.fail("finish the test")

        # 页面更新，清单显示两个待办

        # xx想知道网站是否记住清单
        # 他看到网站生成唯一URL

        # 他访问URL，待办列表还在
        # left with satisfaction


if __name__ == '__main__':
    unittest.main()