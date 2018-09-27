from .base import FunctionalTest
from main.models import Lifemark


class SearchTests(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.login()

    def test_default_search_shows_recent_10_posts(self):
        # augie already has 9 items
        for idx in range(9):
            title = f'existing item {idx}'
            self.add_lifemark(title=title)

        # augie goes to the main page
        self.browser.get(self.live_server_url)

        # main page shows 9 lifemarks in list
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr')
        self.wait_for(
            lambda: self.assertEqual(len(list_trs), 9)
        )

        # augie create 1 more lifemark
        # than main page shows 10 lifemarks in list
        # newly added item is on top of the list
        self.add_lifemark(title='9th item')
        self.check_row_in_list_table(0, '9th item')
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr')
        self.assertEqual(len(list_trs), 10)
        first_row_title = list_trs[0].find_elements_by_xpath('.//td[3]')[0].text
        self.assertEqual(first_row_title, '9th item')

        # augie create 1 more lifemark again
        # than main page still shows 10 lifemarks in list
        # but newly added item is on top of the list
        # and previously last ordered item is not on the list now.
        prev_last_row_title = list_trs[9].find_elements_by_xpath('.//td[2]')[0].text
        self.add_lifemark(title='10th item')
        self.check_row_in_list_table(0, '10th item')
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr')
        self.assertEqual(len(list_trs), 10)
        first_row_title = list_trs[0].find_elements_by_xpath('.//td[3]')[0].text
        self.assertEqual(first_row_title, '10th item')
        title_tds = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr/td[3]')
        self.assertNotIn(prev_last_row_title, [td.text for td in title_tds])

    def test_keyword_search(self):
        # augie has 2 lifemarks
        self.add_lifemark(title='aaa')
        self.add_lifemark(title='bbb')

        # augie goes to the main page
        self.browser.get(self.live_server_url)

        # augie enter single search keyword in search text box
        search_text_box = self.browser.find_element_by_id('id_txt_search')
        search_text_box.send_keys('aaa')
        # he click 'search' button
        self.click_button('id_btn_search')
        self.check_row_in_list_table(0, 'aaa')

        # page updates, and show search result in list and detail table
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_detail_list"]/tbody/tr')
        self.wait_for(
            lambda: self.assertEqual(len(list_trs), 1)
        )

    def test_todo_category_only_search(self):
        # augie has 10 lifemarks and
        # 4 of them are 'todo' category for scheduling
        for i in range(10):
            self.add_lifemark(title=f'existing {i+1}', category=f'category{i*10}')
        for i in range(4):
            lifemark = Lifemark.objects.get(title=f'existing {i+1}')
            lifemark.category = 'todo'
            lifemark.save()

        # augie goes to the main page
        # and he click 'todo search' button
        self.browser.get(self.live_server_url)
        self.click_button('id_btn_search_todo')

        # then page updates, and shows search results only for 4 todo items in list and detail tables
        self.check_detail_row_count(4)
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr')
        self.wait_for(
            lambda: self.assertEqual(len(list_trs), 4)
        )

        # augie now has two 'xxx' keyword item on both 'todo' and non todo category items
        lifemark = Lifemark.objects.get(category='category90')
        lifemark.desc = 'xxx'
        lifemark.save()
        lifemark = Lifemark.objects.filter(category='todo')[0]
        lifemark.desc = 'xxx'
        lifemark.save()

        # augie goes to the main page again
        # he now enter 'xxx' in search text box
        # and click 'todo search'
        self.browser.get(self.live_server_url)
        search_text_box = self.browser.find_element_by_id('id_txt_search')
        search_text_box.send_keys('xxx')
        self.click_button('id_btn_search_todo')

        # then page only shows 'todo' category item with 'xxx'
        self.check_detail_row_count(1)

    def test_ref_category_only_search(self):
        # augie has 10 lifemarks and
        # 4 of them are 'ref' category
        for i in range(10):
            self.add_lifemark(title=f'existing {i+1}', category=f'category{i+10}')
        for i in range(4):
            lifemark = Lifemark.objects.get(title=f'existing {i+1}')
            lifemark.category = 'ref'
            lifemark.save()

        # augie goes to the main page
        # and he click 'ref search' button
        self.browser.get(self.live_server_url)
        self.click_button('id_btn_search_ref')

        # then page updates, and shows search results only for 4 ref items in list and detail tables
        self.check_detail_row_count(4)

        # mixed with keyword is same to 'todo' category search
        # i confirmed to ignore this test
