from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        inputbox = self.browser.find_element_by_id('add_title')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter lifemark title'
        )

        # he types 'new item' into a text box
        inputbox.send_keys('new item')

        # when he hits enter, the page updates
        # and now page lists item he just typed
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
