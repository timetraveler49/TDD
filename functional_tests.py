from selenium import webdriver
import unittest

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
        self.assertIn('To-Do', self.browser.title, "Browser title was " + self.browser.title)

        # 应用有一个输入待办事项的文本输入框

        # 他在文本输入框输入了“Buy flowers”

        # 他按下回车后，页面更新
        # 待办事项表格显示“1:Buy flowers”

        # 页面中游戏那是了一个文本输入框，可以输入其他待办事项
        # 输入"Send a gift to Lisa"

        # 页面更新，清单显示两个待办

        # xx想知道网站是否记住清单
        # 他看到网站生成唯一URL

        # 他访问URL，待办列表还在
        # left with satisfaction


if __name__ == '__main__':
    unittest.main()