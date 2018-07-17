from django.test import LiveServerTestCase
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


class FunctionalTest(LiveServerTestCase):

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
        self.assertIn(text, [row.text for row in rows])

    @wait
    def check_row_in_list_table(self, row, text):
        table = self.browser.find_element_by_id('list_recent')
        rows = table.find_elements_by_tag_name('tr')
        target_row = rows[row]
        self.assertIn(text, target_row.text)

    def click_button(self, id):
        button = self.browser.find_element_by_id(id)
        button.click()

    def click_add_lifemark(self):
        self.click_button('id_btn_add')

    def add_lifemark(self, title):
        inputbox = self.browser.find_element_by_id('id_title')
        inputbox.send_keys(title)
        self.click_add_lifemark()
