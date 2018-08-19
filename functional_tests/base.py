from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
import time

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                # print('>>>>>>>>>>>> error:', e)
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def create_pre_authenticated_session(self, username, password):
        user = User.objects.create_user(
            username=username,
            password=password
        )
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def login(self):
        User.objects.create_user(
            username='augie',
            password='abcde12345',
            email='augie@sample.com'
        )
        self.browser.get(self.live_server_url)
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('augie')
        password_box.send_keys('abcde12345')
        self.click_first_submit()

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def check_is_home_page(self):
        add_form = self.browser.find_element_by_id('id_new_form')
        self.assertNotEqual(add_form, None)

    @wait
    def check_text_in_table(self, text):
        table = self.browser.find_element_by_id('id_recent_list')
        rows = table.find_elements_by_tag_name('tr')
        title_tds = []
        for row in rows:
            tds = row.find_elements_by_tag_name('td')
            title_tds.extend(tds)
        self.assertIn(text, [td.text for td in title_tds])

    @wait
    def check_row_in_list_table(self, row, text):
        table = self.browser.find_element_by_id('id_recent_list')
        tds = table.find_elements_by_xpath(f'.//tbody/tr[{row + 1}]/td')
        self.assertIn(text, [td.text for td in tds])

    @wait
    def check_row_in_detail_table(self, row, field_text_dict):
        table = self.browser.find_element_by_id('id_detail_list')
        tr = table.find_elements_by_xpath(f'.//tbody/tr[{row + 1}]')[0]
        row_id = tr.get_attribute('id')
        id = row_id[row_id.index('_') + 1:]
        td = table.find_elements_by_xpath(f'.//tbody/tr[{row + 1}]/td[1]')[0]
        for field, text in field_text_dict.items():
            actual_text = td.find_element_by_id(f'row_{id}_{field}').text
            self.assertEquals(actual_text, text)

    @wait
    def check_login_required(self):
        self.assertIn('Please login to view your lifemarks', self.browser.find_element_by_id('id_notice').text)

    @wait
    def check_row_count(self, row_count):
        table = self.browser.find_element_by_id('id_recent_list')
        rows = table.find_elements_by_xpath('.//tbody/tr')
        self.assertEqual(len(rows), row_count)

    def click_button(self, id):
        button = self.browser.find_element_by_id(id)
        button.click()

    def click_first_submit(self):
        button = self.browser.find_element_by_tag_name('button')
        button.click()

    def click_add_lifemark(self):
        self.click_button('id_btn_new')

    def click_update_lifemark(self):
        self.click_button('id_btn_update')

    def set_form_input(self, field, value):
        if value:
            input_box = self.browser.find_element_by_id('id_' + field)
            input_box.send_keys(value)

    def add_lifemark(self, title, link=None, category=None, state=None,
                     due_datehour=None, rating=None, tags=None, desc=None,
                     image_url=None):
        self.set_form_input('title', title)
        self.set_form_input('link', link)
        if category:
            category_txt_box = self.browser.find_element_by_id('id_category_txt')
            category_txt_box.send_keys(category)
        if state:
            state_sel = Select(self.browser.find_element_by_id('id_state'))
            state_sel.select_by_value(state)
        if due_datehour:
            due_date = due_datehour[:8]
            due_hour = str(int(due_datehour[8:]))
            due_date_box = self.browser.find_element_by_id('id_due_date')
            due_date_box.send_keys(due_date)
            due_hour_sel = Select(self.browser.find_element_by_id('id_due_hour'))
            due_hour_sel.select_by_visible_text(due_hour)
        self.set_form_input('rating', rating)
        self.set_form_input('tags', tags)
        self.set_form_input('desc', desc)

        self.click_add_lifemark()

    def del_lifemark(self, row_idx):
        table = self.browser.find_element_by_id('id_recent_list')
        tds = table.find_elements_by_xpath(f'.//tbody/tr[{row_idx + 1}]/td[1]')
        target_id = tds[0].text

        list_btn_del = self.browser.find_element_by_id('id_list_btn_del_' + target_id)
        list_btn_del.click()

    def del_lifemark_w_detail_button(self, row_idx):
        table = self.browser.find_element_by_id('id_detail_list')
        tr = table.find_elements_by_xpath(f'.//tbody/tr[{row_idx + 1}]')[0]
        row_id = tr.get_attribute('id')
        target_id = row_id[row_id.index('_') + 1:]

        list_btn_del = self.browser.find_element_by_id('id_detail_btn_del_' + target_id)
        list_btn_del.click()
