from .base import FunctionalTest


class SearchTests(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.login()

    def test_default_search_shows_recent_10_posts(self):
        # augie goes to the main page
        self.browser.get(self.live_server_url)

        # augie add 9 items
        for idx in range(9):
            title = f'existing item {idx}'
            self.add_lifemark(title=title)
            self.check_row_in_list_table(0, title)

        # main page shows 9 lifemarks in list
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr')
        self.wait_for(
            lambda: self.assertEqual(len(list_trs), 9)
        )

        # augie create 1 more lifemark
        # than main page shows 10 lifemarks in list
        # newly added item is on top of the list
        self.add_lifemark(title='9th item')
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr')
        self.assertEqual(len(list_trs), 10)
        first_row_title = list_trs[0].find_elements_by_xpath('.//td[2]')[0].text
        self.assertEqual(first_row_title, '9th item')

        # augie create 1 more lifemark again
        # than main page still shows 10 lifemarks in list
        # but newly added item is on top of the list
        # and previously last ordered item is not on the list now.
        prev_last_row_title = list_trs[9].find_elements_by_xpath('.//td[2]')[0].text
        self.add_lifemark(title='10th item')
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr')
        self.assertEqual(len(list_trs), 10)
        first_row_title = list_trs[0].find_elements_by_xpath('.//td[2]')[0].text
        self.assertEqual(first_row_title, '10th item')
        title_tds = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr/td[2]')
        self.assertNotIn(prev_last_row_title, [td.text for td in title_tds])

    def test_keyword_search(self):
        # augie goes to the main page
        self.browser.get(self.live_server_url)
        # he creates some lifemarks
        self.add_lifemark(title='aaa')
        self.check_row_in_list_table(0, 'aaa')
        self.add_lifemark(title='bbb')
        self.check_row_in_list_table(0, 'bbb')

        # augie enter single search keyword in search text box
        search_text_box = self.browser.find_element_by_id('id_txt_search')
        search_text_box.send_keys('aaa')
        # he click 'search' button
        btn_search = self.browser.find_element_by_id('id_btn_search')
        btn_search.click()

        # page updates, and show search result in list and detail table
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr')
        self.wait_for(
            lambda: self.assertEqual(len(list_trs), 1)
        )
