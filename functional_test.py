from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class BasicInputTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_row_in_list_table(self, text):
        table = self.browser.find_element_by_id('list_recent')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(text, [row.text for row in rows])

    def test_enter_page_and_create_single_item(self):
        # augie enters home page
        self.browser.get('http://localhost:8000')

        # augie notices the page title is Lifemark
        self.assertIn('Lifemark', self.browser.title)

        # augie sees form to insert title of lifemark
        inputbox = self.browser.find_element_by_id('id_add_title')
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

        self.check_row_in_list_table('new item')

        # there's still a text box for insert title of new lifemark
        inputbox = self.browser.find_element_by_id('id_add_title')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter lifemark title'
        )

        # he enters second lifemakr 'second item'
        # end hits enter
        inputbox.send_keys('second item')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # page updates again, and now shows both items on the table list
        self.check_row_in_list_table('new item')
        self.check_row_in_list_table('second item')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
