from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_enter_page_and_create_single_item(self):
        # augie enters home page
        self.browser.get(self.live_server_url)

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

        # page updates again, and now shows both items on the table list
        self.check_row_in_list_table('new item')
        self.check_row_in_list_table('second item')
