from selenium import webdriver
import unittest


class BasicInputTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_enter_page_and_create_single_item(self):
        # augie enters home page
        self.browser.get('http://localhost:8000')

        # augie notices the page title is Lifemark
        self.assertIn('Lifemark', self.browser.title)

        # augie sees form to insert title of lifemark

        # he types 'new item' into a text box

        # when he hits enter, the page updates
        # and now page lists item he just typed


if __name__ == '__main__':
    unittest.main(warnings='ignore')
