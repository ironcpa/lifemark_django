from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


class MainPageTest(FunctionalTest):

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
        category_box = self.browser.find_element_by_id('id_category')
        self.assertEqual(category_box.get_attribute('name'), 'category')
        categorycombo = self.browser.find_element_by_id('id_existing_categories')
        self.assertNotEqual(categorycombo, None)
        #  - is complete
        is_complete_combo = self.browser.find_element_by_id('id_is_complete')
        self.assertEqual(is_complete_combo.get_attribute('name'), 'is_complete')
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
        self.browser.execute_script('fill_category_hidden("sample")')
        Select(is_complete_combo).select_by_value('complete')
        self.browser.execute_script('fill_due_datehour_hidden("2018010100")')
        rating_box.send_keys('xxxxx')
        tags_box.send_keys('aaa bbb')
        desc_box.send_keys('aaaaaaa')
        image_url.send_keys('http://image_location/sample.jpg')

        # he hits 'add lifemark' button
        # page updates, and now he can see just enters lifemark on list
        self.click_add_lifemark()
        self.check_row_in_list_table(0, 'test entry')
        self.check_row_in_list_table(0, 'http://aaa')
        self.fail('expected fail: need to unittest first')

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
