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

    def test_create_lifemark_with_fill_every_form_entries(self):
        # augie enters home page
        self.browser.get(self.live_server_url)

        # augie sees form to create lifemark
        #  - title
        titlebox = self.browser.find_element_by_id('id_title')
        self.assertEqual(titlebox.get_attribute('name'), 'title')
        self.assertEqual(
            titlebox.get_attribute('placeholder'),
            'Enter lifemark title here'
        )
        #  - link
        linkbox = self.browser.find_element_by_id('id_link')
        self.assertEqual(linkbox.get_attribute('name'), 'link')
        self.assertEqual(
            linkbox.get_attribute('placeholder'),
            'Enter related page link'
        )
        #  - category
        categorybox = self.browser.find_element_by_id('id_category')
        self.assertEqual(categorybox.get_attribute('name'), 'category')
        self.assertEqual(
            categorybox.get_attribute('placeholder'),
            'Enter new or select from combo'
        )
        categorycombo = self.browser.find_element_by_id('id_existing_categories')
        self.assertNotEqual(categorycombo, None)
        #  - is complete
        iscompletecombo = self.browser.find_element_by_id('id_is_complete')
        self.assertEqual(iscompletecombo.get_attribute('name'), 'is_complete')
        #  - due date
        duedate_hidden = self.browser.find_element_by_id('id_due_date')
        self.assertEqual(duedate_hidden.get_attribute('name'), 'due_date')
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
        # he hits 'add lifemark' button
        # page updates, and now he can see just enters lifemark on list