from .base import FunctionalTest
from selenium.webdriver.support.select import Select


class MainPageTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.login()
        # below not working
        # self.create_pre_authenticated_session('augie', 'abcde12345')

    def test_enter_page_and_create_single_item(self):
        # augie enters home page
        self.browser.get(self.live_server_url)

        # augie notices the page title is Lifemark
        self.assertIn('Lifemark', self.browser.title)

        # augie sees form to insert title of lifemark
        inputbox = self.browser.find_element_by_id('id_title')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter lifemark title'
        )

        # he types 'new item' into a text box
        inputbox.send_keys('new item')

        # when he click 'add lifemark' button
        # the page updates and now page lists item he just typed
        self.click_add_lifemark()

        self.check_text_in_table('new item')

        # there's still a text box for insert title of new lifemark
        inputbox = self.browser.find_element_by_id('id_title')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter lifemark title'
        )

        # he enters second lifemakr 'second item'
        # end hits enter
        inputbox.send_keys('second item')
        self.click_add_lifemark()

        # page updates again, and now shows both items on the table list
        self.check_text_in_table('new item')
        self.check_text_in_table('second item')

    def test_create_lifemark_with_fill_every_form_entries(self):
        # augie enters home page
        self.browser.get(self.live_server_url)

        # augie sees form to create lifemark
        #  - title
        title_box = self.browser.find_element_by_id('id_title')
        self.assertEqual(title_box.get_attribute('name'), 'title')
        self.assertEqual(
            title_box.get_attribute('placeholder'),
            'Enter lifemark title'
        )
        #  - link
        link_box = self.browser.find_element_by_id('id_link')
        self.assertEqual(link_box.get_attribute('name'), 'link')
        self.assertEqual(
            link_box.get_attribute('placeholder'),
            'Enter related page link'
        )
        #  - category
        category_box = self.browser.find_element_by_id('id_category_txt')
        self.assertNotEqual(category_box, None)
        categorycombo = self.browser.find_element_by_id('id_category_sel')
        self.assertNotEqual(categorycombo, None)
        #  - is complete
        state_combo = self.browser.find_element_by_id('id_state')
        self.assertEqual(state_combo.get_attribute('name'), 'state')
        #  - due date
        duedate_box = self.browser.find_element_by_id('id_due_date')
        self.assertNotEqual(duedate_box, None)
        due_hour_combo = self.browser.find_element_by_id('id_due_hour')
        self.assertNotEqual(due_hour_combo, None)
        duedate_hidden = self.browser.find_element_by_id('id_due_datehour')
        self.assertEqual(duedate_hidden.get_attribute('name'), 'due_datehour')
        #  - rating
        rating_box = self.browser.find_element_by_id('id_rating')
        self.assertEqual(rating_box.get_attribute('name'), 'rating')
        #  - tags
        tags_box = self.browser.find_element_by_id('id_tags')
        self.assertEqual(tags_box.get_attribute('name'), 'tags')
        #  - descriptions
        desc_box = self.browser.find_element_by_id('id_desc')
        self.assertEqual(desc_box.get_attribute('name'), 'desc')
        #  - image
        image_url = self.browser.find_element_by_id('id_image_url')
        self.assertNotEqual(image_url, None)

        # augie fills in all entries
        title_box.send_keys('test entry')
        link_box.send_keys('http://aaa')
        category_box.send_keys('test cate')
        Select(state_combo).select_by_value('complete')
        duedate_box.send_keys('20180801')
        Select(due_hour_combo).select_by_value('0')
        rating_box.send_keys('xxxxx')
        tags_box.send_keys('aaa bbb')
        desc_box.send_keys('aaaaaaa')
        image_url.send_keys('http://image_location/sample.jpg')

        # he hits 'add lifemark' button
        # page updates, and now he can see just enters lifemark on list
        self.click_add_lifemark()

        self.check_row_in_detail_table(0, {
            'title': 'test entry',
            'link': 'http://aaa',
            'category': 'test cate',
            'state': 'complete',
            'due_datehour': '2018080100',
            'rating': 'xxxxx',
            'tags': 'aaa bbb',
            'desc': 'aaaaaaa',
            'image_url': 'http://image_location/sample.jpg'
        })

    def test_cannot_add_empty_titled_lifemark(self):
        # augie goes to the main page
        # with empty title, he clicks 'add lifemark' button
        self.browser.get(self.live_server_url)
        title_box = self.browser.find_element_by_id('id_title')
        self.click_add_lifemark()

        # the browser intercepts the request, shows validation error
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_title:invalid'
        ))

        # he type some title, then validation error disappears
        title_box.send_keys('new item')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_title:valid'
        ))

        # and he can submit with 'add lifemark' as expected
        self.click_add_lifemark()
        self.check_text_in_table('new item')

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
            due_datehour='2018010100',
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
        edit_due_date_box = update_form.find_element_by_id('id_due_date')
        edit_due_hour_sel = Select(update_form.find_element_by_id('id_due_hour'))
        edit_desc_box = update_form.find_element_by_id('id_desc')

        self.assertEqual(edit_title_box.get_attribute('value'), 'existing item 2')
        self.assertEqual(edit_link_box.get_attribute('value'), 'http://aaa.bbb.com')
        self.assertEqual(edit_category_sel.first_selected_option.text, 'initial category')
        self.assertEqual(edit_state_sel.first_selected_option.text, 'todo')
        self.assertEqual(edit_due_date_box.get_attribute('value'), '20180101')
        self.assertEqual(edit_due_hour_sel.first_selected_option.text, '0')
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
            due_datehour='2018010100',
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
        edit_due_date_box = update_form.find_element_by_id('id_due_date')
        edit_due_hour_sel = Select(update_form.find_element_by_id('id_due_hour'))
        edit_desc_box = update_form.find_element_by_id('id_desc')

        self.assertEqual(edit_title_box.get_attribute('value'), 'existing item 2')
        self.assertEqual(edit_link_box.get_attribute('value'), 'http://aaa.bbb.com')
        self.assertEqual(edit_category_sel.first_selected_option.text, 'initial category')
        self.assertEqual(edit_state_sel.first_selected_option.text, 'todo')
        self.assertEqual(edit_due_date_box.get_attribute('value'), '20180101')
        self.assertEqual(edit_due_hour_sel.first_selected_option.text, '0')
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
            due_datehour='2018010100',
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
        edit_due_date_box = update_form.find_element_by_id('id_due_date')
        edit_due_hour_sel = Select(update_form.find_element_by_id('id_due_hour'))
        edit_desc_box = update_form.find_element_by_id('id_desc')

        self.wait_for(
            lambda: self.assertEqual(edit_title_box.get_attribute('value'), 'existing item 2')
        )
        self.assertEqual(edit_link_box.get_attribute('value'), 'http://aaa.bbb.com')
        self.assertEqual(edit_category_sel.first_selected_option.text, 'initial category')
        self.assertEqual(edit_state_sel.first_selected_option.text, 'todo')
        self.assertEqual(edit_due_date_box.get_attribute('value'), '20180101')
        self.assertEqual(edit_due_hour_sel.first_selected_option.text, '0')
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

    def test_delete_lifemark(self):
        # augie goes to the main page
        # this page has already existing 2 lifemarks
        self.create_lifemark_on_db(title='existing item 1')
        self.create_lifemark_on_db(title='existing item 2')
        self.browser.get(self.live_server_url)

        # augie click 'del' button on list
        # then page updates, and now clicked item is disappeared
        self.del_lifemark(0)

        self.check_row_in_list_table(0, 'existing item 1')
        self.check_row_count(1)

        # augie click 'del' button on the other item
        # then page updates, and there're no items in list table
        self.del_lifemark(0)

        self.check_row_count(0)

    def test_delete_lifemark_w_detail_button(self):
        # augie goes to the main page
        # this page has already existing 2 lifemarks
        self.create_lifemark_on_db(title='existing item 1')
        self.create_lifemark_on_db(title='existing item 2')
        self.browser.get(self.live_server_url)

        # augie click 'del' button on detail list
        # then page updates, and now clicked item is disappeared
        self.del_lifemark_w_detail_button(0)

        self.check_row_in_list_table(0, 'existing item 1')
        self.check_row_count(1)

        # augie click 'del' button on the other item
        # then page updates, and there're no items in list table
        self.del_lifemark_w_detail_button(0)

        self.check_row_count(0)
