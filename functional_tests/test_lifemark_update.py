from .base import FunctionalTest
from selenium.webdriver.support.select import Select


class LifemarkUpdateTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.login()

    def test_update_existing_lifemark(self):
        # augie goes to the main page
        # this page has already existing lifemarks
        self.create_lifemark_on_db(
            title='existing item 1',
            category='other category'
        )
        self.create_lifemark_on_db(
            title='existing item 2',
            link='http://aaa.bbb.com',
            category='initial category',
            state='todo',
            due_datehour='2018-01-02 03',
            rating='x',
            tags='aaa',
            desc='initial desc 1',
            image_url='http://aaa.com/sample.jpg'
        )
        self.browser.get(self.live_server_url)

        # augie click 'edit' button on list's 1st row
        self.click_list_button(0, 'edit')

        # then edit form is shown instead of add form
        # and clicked item's fields are shown on form fields
        update_form = self.browser.find_element_by_id('id_update_form')

        edit_title_box = update_form.find_element_by_id('id_title')
        edit_link_box = update_form.find_element_by_id('id_link')
        edit_category_sel = Select(update_form.find_element_by_id('id_category_sel'))
        edit_state_sel = Select(update_form.find_element_by_id('id_state'))
        edit_due_date_box = update_form.find_element_by_id('id_update_due_date')
        edit_due_hour_sel = Select(update_form.find_element_by_id('id_due_hour'))
        edit_desc_box = update_form.find_element_by_id('id_desc')

        self.assertEqual(edit_title_box.get_attribute('value'), 'existing item 2')
        self.assertEqual(edit_link_box.get_attribute('value'), 'http://aaa.bbb.com')
        self.assertEqual(edit_category_sel.first_selected_option.text, 'initial category')
        self.assertEqual(edit_state_sel.first_selected_option.text, 'todo')
        self.assertEqual(edit_due_date_box.get_attribute('value'), '2018-01-02')
        self.assertEqual(edit_due_hour_sel.first_selected_option.text, '3')
        self.assertEqual(edit_desc_box.get_attribute('value'), 'initial desc 1')

        # he modify some fields and click 'update' button
        # page updates, and now he can see updated data on the list
        edit_title_box.clear()
        edit_title_box.send_keys('modified item')
        edit_category_sel.select_by_value('other category')
        edit_desc_box.clear()
        edit_desc_box.send_keys('modified desc')
        self.click_update_lifemark()

        # self.check_text_in_table('modified item')
        self.check_row_in_detail_table(0, {
            'title': 'modified item',
            'category': 'other category',
            'desc': 'modified desc'
        })

    def test_update_existing_lifemark_w_category_txt(self):
        # augie goes to the main page
        # this page has already existing lifemarks
        self.create_lifemark_on_db(title='existing item 1')
        self.create_lifemark_on_db(
            title='existing item 2',
            link='http://aaa.bbb.com',
            category='initial category',
            state='todo',
            due_datehour='2018-01-02 03',
            rating='x',
            tags='aaa',
            desc='initial desc 1',
            image_url='http://aaa.com/sample.jpg'
        )
        self.browser.get(self.live_server_url)

        # augie click 'edit' button on list's 1st row
        self.click_list_button(0, 'edit')

        # then edit form is shown instead of add form
        # and clicked item's fields are shown on form fields
        update_form = self.browser.find_element_by_id('id_update_form')

        edit_title_box = update_form.find_element_by_id('id_title')
        edit_link_box = update_form.find_element_by_id('id_link')
        edit_category_sel = Select(update_form.find_element_by_id('id_category_sel'))
        edit_category_txt = update_form.find_element_by_id('id_category_txt')
        edit_state_sel = Select(update_form.find_element_by_id('id_state'))
        edit_due_date_box = update_form.find_element_by_id('id_update_due_date')
        edit_due_hour_sel = Select(update_form.find_element_by_id('id_due_hour'))
        edit_desc_box = update_form.find_element_by_id('id_desc')

        self.assertEqual(edit_title_box.get_attribute('value'), 'existing item 2')
        self.assertEqual(edit_link_box.get_attribute('value'), 'http://aaa.bbb.com')
        self.assertEqual(edit_category_sel.first_selected_option.text, 'initial category')
        self.assertEqual(edit_state_sel.first_selected_option.text, 'todo')
        self.assertEqual(edit_due_date_box.get_attribute('value'), '2018-01-02')
        self.assertEqual(edit_due_hour_sel.first_selected_option.text, '3')
        self.assertEqual(edit_desc_box.get_attribute('value'), 'initial desc 1')

        # he modify some fields and click 'update' button
        # page updates, and now he can see updated data on the list
        edit_title_box.clear()
        edit_title_box.send_keys('modified item')
        edit_category_txt.send_keys('modified category')
        edit_desc_box.clear()
        edit_desc_box.send_keys('modified desc')
        self.click_update_lifemark()

        # self.check_text_in_table('modified item')
        self.check_row_in_detail_table(0, {
            'title': 'modified item',
            'category': 'modified category',
            'desc': 'modified desc'
        })

    def test_update_existing_lifemark_w_detail_button(self):
        # augie goes to the main page
        # this page has already existing lifemarks
        self.create_lifemark_on_db(title='existing item 1')
        self.create_lifemark_on_db(
            title='existing item 2',
            link='http://aaa.bbb.com',
            category='initial category',
            state='todo',
            due_datehour='2018-01-02 03',
            rating='x',
            tags='aaa',
            desc='initial desc 1',
            image_url='http://aaa.com/sample.jpg'
        )
        self.browser.get(self.live_server_url)

        # augie click 'edit' button on detail list
        table = self.browser.find_element_by_id('id_recent_list')
        tds = table.find_elements_by_xpath('.//tbody/tr[1]/td')
        target_id = tds[0].text

        detail_btn_edit = self.browser.find_element_by_id('id_detail_btn_edit_' + target_id)
        detail_btn_edit.click()

        # then edit form is shown instead of add form
        # and clicked item's fields are shown on form fields
        update_form = self.browser.find_element_by_id('id_update_form')

        edit_title_box = update_form.find_element_by_id('id_title')
        edit_link_box = update_form.find_element_by_id('id_link')
        edit_category_sel = Select(update_form.find_element_by_id('id_category_sel'))
        edit_state_sel = Select(update_form.find_element_by_id('id_state'))
        edit_due_date_box = update_form.find_element_by_id('id_update_due_date')
        edit_due_hour_sel = Select(update_form.find_element_by_id('id_due_hour'))
        edit_desc_box = update_form.find_element_by_id('id_desc')

        self.wait_for(
            lambda: self.assertEqual(edit_title_box.get_attribute('value'), 'existing item 2')
        )
        self.assertEqual(edit_link_box.get_attribute('value'), 'http://aaa.bbb.com')
        self.assertEqual(edit_category_sel.first_selected_option.text, 'initial category')
        self.assertEqual(edit_state_sel.first_selected_option.text, 'todo')
        self.assertEqual(edit_due_date_box.get_attribute('value'), '2018-01-02')
        self.assertEqual(edit_due_hour_sel.first_selected_option.text, '3')
        self.assertEqual(edit_desc_box.get_attribute('value'), 'initial desc 1')

        # he modify some fields and click 'update' button
        # page updates, and now he can see updated data on the list
        edit_title_box.clear()
        edit_title_box.send_keys('modified item')
        edit_desc_box.clear()
        edit_desc_box.send_keys('modified desc')
        self.click_update_lifemark()

        # self.check_text_in_table('modified item')
        self.check_row_in_detail_table(0, {'title': 'modified item', 'desc': 'modified desc'})
