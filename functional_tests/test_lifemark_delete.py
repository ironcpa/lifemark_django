from .base import FunctionalTest


class LifemarkDeleteTest(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.login()

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
