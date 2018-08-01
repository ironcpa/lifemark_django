from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def check_text_in_table(self, text):
        table = self.browser.find_element_by_id('list_recent')
        rows = table.find_elements_by_tag_name('tr')
        title_tds = []
        for row in rows:
            tds = row.find_elements_by_tag_name('td')
            title_tds.extend(tds)
        self.assertIn(text, [td.text for td in title_tds])

    @wait
    def check_row_in_list_table(self, row, text):
        table = self.browser.find_element_by_id('list_recent')
        rows = table.find_elements_by_tag_name('tr')
        tds = rows[row].find_elements_by_tag_name('td')
        self.assertIn(text, [td.text for td in tds])

    @wait
    def check_row_count(self, row_count):
        table = self.browser.find_element_by_id('list_recent')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), row_count)

    def click_button(self, id):
        button = self.browser.find_element_by_id(id)
        button.click()

    def click_add_lifemark(self):
        self.click_button('id_btn_add')

    def click_update_lifemark(self):
        self.click_button('id_btn_update')

    def add_lifemark(self, title):
        inputbox = self.browser.find_element_by_id('id_title')
        inputbox.send_keys(title)
        self.click_add_lifemark()

    def del_lifemark(self, row_idx):
        table = self.browser.find_element_by_id('list_recent')
        rows = table.find_elements_by_tag_name('tr')
        target_row = rows[row_idx]
        row_id = target_row.get_attribute('id')
        target_id = row_id[row_id.index('_') + 1:]

        list_btn_del = self.browser.find_element_by_id('id_list_btn_del_' + target_id)
        list_btn_del.click()
