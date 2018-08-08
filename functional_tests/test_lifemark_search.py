from .base import FunctionalTest


class SearchTests(FunctionalTest):

    def test_default_search_shows_recent_10_posts(self):
        # augie goes to the main page
        self.browser.get(self.live_server_url)

        # augie add 9 items
        for idx in range(9):
            self.add_lifemark(title=f'existing item {idx}')

        # main page shows 9 lifemarks in list
        list_trs = self.browser.find_elements_by_xpath('//table[@id="id_recent_list"]/tbody/tr')
        self.assertEqual(len(list_trs), 9)

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

    def test_basic_search(self):
        pass
