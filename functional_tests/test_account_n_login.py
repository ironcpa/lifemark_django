from .base import FunctionalTest
from django.contrib.auth.models import User


class AccountAndLoginTest(FunctionalTest):

    def test_non_member_sign_up(self):
        # non member augie enters home page
        # he only found 'Please Login to view your lifemarks' on the page
        self.browser.get(self.live_server_url)
        self.check_login_required()

        # he click 'Signup' button
        # page update and he can see signup form
        # there's id, password, email input boxes
        self.click_button('id_btn_signup')
        user_name_box = self.browser.find_element_by_id('id_username')
        user_password_box = self.browser.find_element_by_id('id_password1')
        user_password_check_box = self.browser.find_element_by_id('id_password2')
        user_email_box = self.browser.find_element_by_id('id_email')

        # if he doesn't fill in all fields
        # page shows validation errors

        # he fill in fields and click 'Ok' button
        # then page updates and he automatically logged in
        # he can find his id is shown on top-right side of the page
        user_name_box.send_keys('augie')
        user_password_box.send_keys('abcde12345')
        user_password_check_box.send_keys('abcde12345')
        user_email_box.send_keys('augie@aaa.bbb')
        self.click_first_submit()

        self.wait_for(
            lambda: self.assertEquals('augie logged in', self.browser.find_element_by_id('id_logged_in_user').text)
        )

        # and hee can see lifemarks home page with forms
        self.check_is_home_page()

    def test_member_login(self):
        # member augie has account
        '''
        User.objects.create_user(
            username='augie',
            password='abcde12345',
            email='augie@sample.com'
        )
        '''
        self.browser.get(self.live_server_url + '/test_create_user?username=augie&password=abcde12345')

        # member augie enters home page
        # he only found 'Please Login to view your lifemarks' on the page
        self.browser.get(self.live_server_url)
        self.check_login_required()

        # he click 'Login' button
        # page updates and he can see login form
        # there's id, password fieids
        self.click_button('id_btn_login')
        self.wait_for(
            lambda: self.browser.find_element_by_id('id_username')
        )
        self.wait_for(
            lambda: self.browser.find_element_by_id('id_password')
        )

        # if he doen't fill in all fields
        # page shows validatio errors
        self.click_first_submit()
        self.wait_for(
            lambda: self.browser.find_element_by_id('id_username')
        )
        self.wait_for(
            lambda: self.browser.find_element_by_id('id_password')
        )
        self.wait_for(
            lambda: self.browser.find_element_by_class_name('errorlist')
        )

        # he fill in fields and click 'Ok' button
        # then page updates and he can see lifemarks functionality on page
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('augie')
        password_box.send_keys('abcde12345')
        self.click_first_submit()

        self.check_is_home_page()
