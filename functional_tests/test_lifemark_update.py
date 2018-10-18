from .base import FunctionalTest
from selenium.webdriver.support.select import Select


class LifemarkUpdateTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.login()

    def test_update_existing_lifemark(self):
        # augie goes to the main page
        # this page has already existing lifemarks
        self.add_lifemark(
            title='existing item 1',
            category='other category'
        )
        self.add_lifemark(
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
        self.check_row_count(2)

        # augie click 'edit' button on list's 1st row
        self.click_list_button(0, 'edit')

        # then edit form is shown instead of add form
        # and clicked item's fields are shown on form fields
        self.check_form(self.browser.find_element_by_id('id_update_form'),
                        title='existing item 2',
                        link='http://aaa.bbb.com',
                        category='initial category',
                        state='todo',
                        due_datehour='2018-01-02 03',
                        desc='initial desc 1')

        # he modify some fields and click 'update' button
        # page updates, and now he can see updated data on the list
        self.update_lifemark_w_ui(0,
                                  title='modified item',
                                  category='other category',
                                  desc='modified desc')

        # self.check_text_in_table('modified item')
        self.check_row_in_detail_table(0, {
            'title': 'modified item',
            'category': 'other category',
            'desc': 'modified desc'
        })

    def test_update_existing_lifemark_w_category_txt(self):
        # augie goes to the main page
        # this page has already existing lifemarks
        self.add_lifemark(title='existing item 1')
        self.add_lifemark(
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
        self.check_row_count(2)

        # augie click 'edit' button on list's 1st row
        self.click_list_button(0, 'edit')

        # then edit form is shown instead of add form
        # and clicked item's fields are shown on form fields
        self.check_form(self.browser.find_element_by_id('id_update_form'),
                        title='existing item 2',
                        link='http://aaa.bbb.com',
                        category='initial category',
                        state='todo',
                        due_datehour='2018-01-02 03',
                        desc='initial desc 1')

        # he modify some fields and click 'update' button
        # page updates, and now he can see updated data on the list
        self.update_lifemark_w_ui(0,
                                  title='modified item',
                                  category='modified category',
                                  desc='modified desc')

        # self.check_text_in_table('modified item')
        self.check_row_in_detail_table(0, {
            'title': 'modified item',
            'category': 'modified category',
            'desc': 'modified desc'
        })

    def test_update_existing_lifemark_w_detail_button(self):
        # augie goes to the main page
        # this page has already existing lifemarks
        self.add_lifemark(title='existing item 1')
        self.add_lifemark(
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
        self.check_row_count(2)

        # augie click 'edit' button on detail list
        table = self.browser.find_element_by_id('id_recent_list')
        tds = table.find_elements_by_xpath('.//tbody/tr[1]/td')
        target_id = tds[0].text

        detail_btn_edit = self.browser.find_element_by_id('id_detail_btn_edit_' + target_id)
        detail_btn_edit.click()

        # then edit form is shown instead of add form
        # and clicked item's fields are shown on form fields
        self.check_form(self.browser.find_element_by_id('id_update_form'),
                        title='existing item 2',
                        link='http://aaa.bbb.com',
                        category='initial category',
                        state='todo',
                        due_datehour='2018-01-02 03',
                        desc='initial desc 1')

        # he modify some fields and click 'update' button
        # page updates, and now he can see updated data on the list
        self.update_lifemark_w_ui(0,
                                  title='modified item',
                                  desc='modified desc')

        # self.check_text_in_table('modified item')
        self.check_row_in_detail_table(0, {'title': 'modified item', 'desc': 'modified desc'})
