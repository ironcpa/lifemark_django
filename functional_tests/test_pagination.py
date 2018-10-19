from .base import FunctionalTest, wait


class PageNavigationTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.login()

    def curr_page_format(self, page_num):
        return f'{page_num}\n(current)'

    def get_all_page_links(self):
        page_parent = self.browser.find_element_by_class_name('pagination')
        page_links = page_parent.find_elements_by_tag_name('li')

        return page_links

    def is_number_page_link(self, link_node):
        return link_node.text not in ['First', 'Prev', 'Next', 'Last']

    def get_curr_page_link(self):
        for link in self.get_all_page_links():
            if link.get_attribute('class') == 'active':
                return link

    def get_page_link(self, link_text):
        for link in self.get_all_page_links():
            if link.text == link_text:
                return link

    def click_page_link(self, link_text):
        link_text = str(link_text)
        target_link = self.get_page_link(link_text)
        if target_link:
            anchor = target_link.find_element_by_tag_name('a')
            if anchor:
                anchor.click()

    @wait
    def check_curr_page(self, page_num):
        link_text = self.curr_page_format(page_num)
        self.assertEqual(
            self.get_curr_page_link().text,
            self.get_page_link(link_text).text
        )

    @wait
    def check_num_page_link_count(self, page_count):
        counter = 0
        for link in self.get_all_page_links():
            if self.is_number_page_link(link):
                counter += 1
        self.assertEqual(counter, page_count)

    def test_next_gets_next_n_page_links(self):
        # augie already has 250 items: it's 25 pages
        for i in range(250):
            self.add_lifemark(title=f'item {i}')

        # he goes to the main page
        self.browser.get(self.live_server_url)
        self.check_row_count(10)

        # and can see first 11 page links:
        #   - app uses range pagination
        #   - currpage + prev_range(5) + next_range(5)
        #   - if curr is 1st or last, still shows 5 * 2 pages links
        self.check_num_page_link_count(11)
        self.assertEqual(
            self.get_curr_page_link().text,
            self.curr_page_format(1)
        )

        # if he click 'next' link
        # curr page is 2
        self.click_page_link('Next')
        self.check_curr_page(2)

        # augie goes to the first page to test freshly
        # and he click last number(11) link
        # he can see 11th page is current
        # and curr(11th) page is centered in page links
        # and can see 11 links on page
        self.click_page_link(1)
        self.check_curr_page(1)

        self.click_page_link(11)
        self.check_curr_page(11)

        self.check_num_page_link_count(11)
