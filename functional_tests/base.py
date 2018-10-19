from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
import time
import os

# from django.conf import settings
# from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.auth.models import User
# from django.contrib.sessions.backends.db import SessionStore

from main.models import Lifemark

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException, IndexError) as e:
                # print('>>>>>>>>>>>> error:', e)
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        # todo: profile move to class level
        # # ==============================================
        # geolocation option for firefox
        profile = webdriver.FirefoxProfile()
        # allow location data ----------------------------
        profile.set_preference("geo.prompt.testing", True)
        profile.set_preference("geo.prompt.testing.allow", True)
        # # === can force location data ------------------
        # profile.set_preference('geo.wifi.uri', 'firefox_geo_test_setting.json')
        # # === disable geolocation: for faster test -----
        # profile.set_preference("geo.enabled", False)

        self.browser = webdriver.Firefox(firefox_profile=profile)

        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = staging_server
            self.is_remote_test = True
        else:
            self.is_remote_test = False

    def tearDown(self):
        self.browser.quit()

    def create_pre_authenticated_session(self, username, password, email):
        """this isn't working as intended
        can't pass @login_required on view
        """
        '''
        # create user in db
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # set session_key on server
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        # set same session_key on browser
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))
        '''
        self.browser.get(self.live_server_url + '/test_login?username=testxxx&password=1234')

    def login(self):
        User.objects.create_user(
            username='augie',
            password='abcde12345',
            email='augie@sample.com'
        )
        self.browser.get(self.live_server_url)
        self.check_login_required()

        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('augie')
        password_box.send_keys('abcde12345')
        self.click_first_submit()

        '''
        self.create_pre_authenticated_session(
            'augie',
            'abcde12345',
            'augie@sample.com'
        )
        '''

    @wait
    def wait_for_single(self, fn):
        return fn()

    def wait_for(self, *fns):
        for fn in fns:
            return self.wait_for_single(fn)

    @wait
    def get_first_row_id(self):
        table = self.browser.find_element_by_id('id_recent_list')
        first_id_td = table.find_element_by_xpath(f'.//tbody/tr[1]/td[1]')
        return int(first_id_td.text)

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
            if field == 'id':
                self.assertEqual(id, text)
            else:
                span = td.find_element_by_id(f'row_{id}_{field}')
                if span.is_displayed():
                    actual_text = span.text
                else:
                    actual_text = span.get_attribute('innerHTML')
                self.assertEquals(actual_text, text)

    @wait
    def check_login_required(self):
        self.assertIn('Please login to view your lifemarks', self.browser.find_element_by_id('id_notice').text)

    @wait
    def check_row_count(self, row_count):
        table = self.browser.find_element_by_id('id_detail_list')
        rows = table.find_elements_by_xpath('.//tbody/tr')
        self.assertEqual(len(rows), row_count)

    @wait
    def check_form(self,
                   target_form,
                   title=None, link=None, category=None, state=None,
                   due_datehour=None, desc=None):
        edit_title_box = target_form.find_element_by_id('id_title')
        edit_link_box = target_form.find_element_by_id('id_link')
        edit_category_sel = Select(target_form.find_element_by_id('id_category_sel'))
        edit_state_sel = Select(target_form.find_element_by_id('id_state'))
        edit_due_date_box = target_form.find_element_by_id('id_update_due_date')
        edit_due_hour_sel = Select(target_form.find_element_by_id('id_due_hour'))
        edit_desc_box = target_form.find_element_by_id('id_desc')

        if title:
            self.assertEqual(edit_title_box.get_attribute('value'), title)
        if link:
            self.assertEqual(edit_link_box.get_attribute('value'), link)
        if category:
            self.assertEqual(edit_category_sel.first_selected_option.text, category)
        if state:
            self.assertEqual(edit_state_sel.first_selected_option.text, state)
        if due_datehour:
            due_date = due_datehour[:10]
            due_hour = str(int(due_datehour[11:]))
            self.assertEqual(edit_due_date_box.get_attribute('value'), due_date)
            self.assertEqual(edit_due_hour_sel.first_selected_option.text, due_hour)
        if desc:
            self.assertEqual(edit_desc_box.get_attribute('value'), desc)

    @wait
    def check_detail_row_count(self, row_count):
        detail_trs = self.browser.find_elements_by_xpath('//table[@id="id_detail_list"]/tbody/tr')
        self.assertEqual(len(detail_trs), row_count)

    def get_row_id(self, row):
        table = self.browser.find_element_by_id('id_detail_list')
        tds = table.find_elements_by_xpath(f'.//tbody/tr[{row + 1}]/td')
        target_id = tds[0].text

        return target_id

    def click_button(self, id):
        button = self.browser.find_element_by_id(id)
        button.click()

    def click_list_button(self, row, btn_type):
        table = self.browser.find_element_by_id('id_detail_list')
        tr = table.find_elements_by_xpath(f'.//tbody/tr[{row + 1}]')[0]
        row_id = tr.get_attribute('id')
        target_id = row_id[row_id.index('_') + 1:]

        list_btn_edit = self.browser.find_element_by_id(f'id_list_btn_{btn_type}_' + target_id)
        list_btn_edit.click()

    def click_first_submit(self):
        # button = self.browser.find_element_by_tag_name('button')
        button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        button.click()

    def click_add_lifemark(self):
        self.click_button('id_btn_new')

    def click_update_lifemark(self):
        self.click_button('id_btn_update')

    def set_form_input(self, field, value, target_form=None):
        if not target_form:
            target_form = self.browser.find_element_by_id('id_new_form')

        if value:
            input_box = target_form.find_element_by_id('id_' + field)
            input_box.clear()
            input_box.send_keys(value)

    def add_lifemark_w_ui(self, title, link=None, category=None, state=None,
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
            due_date = due_datehour[:10]
            due_hour = str(int(due_datehour[10:]))
            due_date_box = self.browser.find_element_by_id('id_due_date')
            due_date_box.send_keys(due_date)
            due_hour_sel = Select(self.browser.find_element_by_id('id_due_hour'))
            due_hour_sel.select_by_visible_text(due_hour)
        self.set_form_input('rating', rating)
        self.set_form_input('tags', tags)
        self.set_form_input('desc', desc)

        self.click_add_lifemark()

        self.check_row_in_detail_table(0, {'title': title})

    def update_lifemark_w_ui(self, row_idx, title=None, link=None, category=None, state=None,
                             due_datehour=None, rating=None, tags=None, desc=None,
                             image_url=None):
        self.click_list_button(row_idx, 'edit')

        update_form = self.browser.find_element_by_id('id_update_form')

        self.set_form_input('title', title, update_form)
        self.set_form_input('link', link, update_form)
        if category:
            category_txt_box = update_form.find_element_by_id('id_category_txt')
            category_txt_box.send_keys(category)
        if state:
            state_sel = Select(update_form.find_element_by_id('id_state'))
            state_sel.select_by_value(state)
        if due_datehour:
            due_date = due_datehour[:10]
            due_hour = str(int(due_datehour[10:]))
            due_date_box = update_form.find_element_by_id('id_due_date')
            due_date_box.send_keys(due_date)
            due_hour_sel = Select(update_form.find_element_by_id('id_due_hour'))
            due_hour_sel.select_by_visible_text(due_hour)
        self.set_form_input('rating', rating, update_form)
        self.set_form_input('tags', tags, update_form)
        self.set_form_input('desc', desc, update_form)

        self.click_update_lifemark()

        # need to check from caller location to check page update correctly

    def add_lifemark(self, title, link=None, category=None, state=None,
                     due_datehour=None, rating=None, tags=None, desc=None,
                     image_url=None):
        if self.is_remote_test:
            self.add_lifemark_w_ui(title, link, category, state,
                                   due_datehour, rating, tags, desc,
                                   image_url)
        else:
            lifemark = Lifemark.objects.create(title=title)
            if link:
                lifemark.link = link
            if category:
                lifemark.category = category
            if state:
                lifemark.state = state
            if due_datehour:
                lifemark.due_datehour = due_datehour
            if tags:
                lifemark.tags = tags
            if desc:
                lifemark.desc = desc
            if image_url:
                lifemark.image_url = image_url
            lifemark.save()

    def update_lifemark(self, id, title=None, link=None, category=None, state=None,
                        due_datehour=None, rating=None, tags=None, desc=None,
                        image_url=None):
        if self.is_remote_test:
            self.update_lifemark_w_ui(id, title, link, category, state,
                                      due_datehour, rating, tags, desc,
                                      image_url)
        else:
            lifemark = Lifemark.objects.get(id=id)
            if title:
                lifemark.title = title
            if link:
                lifemark.link = link
            if category:
                lifemark.category = category
            if state:
                lifemark.state = state
            if due_datehour:
                lifemark.due_datehour = due_datehour
            if tags:
                lifemark.tags = tags
            if desc:
                lifemark.desc = desc
            if image_url:
                lifemark.image_url = image_url
            lifemark.save()

    def del_lifemark(self, row_idx):
        table = self.browser.find_element_by_id('id_recent_list')
        tds = table.find_elements_by_xpath(f'.//tbody/tr[{row_idx + 1}]/td[1]')
        target_id = tds[0].text

        list_btn_del = self.browser.find_element_by_id('id_list_btn_del_' + target_id)
        list_btn_del.click()
        alert = self.browser.switch_to_alert()
        alert.accept()

    def del_lifemark_w_detail_button(self, row_idx):
        table = self.browser.find_element_by_id('id_detail_list')
        tr = table.find_elements_by_xpath(f'.//tbody/tr[{row_idx + 1}]')[0]
        row_id = tr.get_attribute('id')
        target_id = row_id[row_id.index('_') + 1:]

        list_btn_del = self.browser.find_element_by_id('id_detail_btn_del_' + target_id)
        list_btn_del.click()
        alert = self.browser.switch_to_alert()
        alert.accept()
