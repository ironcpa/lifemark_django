from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..views import signup
from ..forms import SignupForm


class SignupTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_exists(self):
        url = reverse('signup')
        view = resolve(url)
        self.assertEquals(view.func, signup)

    def test_signup_template(self):
        self.assertTemplateUsed(self.response, 'signup.html')

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_uses_expected_form(self):
        form = self.response.context.get('form')
        self.assertIn('username', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        self.assertIn('email', form.fields)
        self.assertIsInstance(self.response.context['form'], SignupForm)

    def test_has_user_before_login(self):
        user = self.response.context.get('user')
        self.assertNotEquals(user, None)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignupTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'augie',
            'email': 'augie@sample.com',
            'password1': 'abcde123456',
            'password2': 'abcde123456',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection_after_signup(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        res = self.client.get(self.home_url)
        user = res.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignupTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


class LoginTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='augie',
            password='abcde123456',
            email='augie@sample.com'
        )

        url = reverse('login')
        data = {
            'username': 'augie',
            'password': 'abcde123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection_after_login(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_authentication(self):
        res = self.client.get(self.home_url)
        user = res.context.get('user')
        self.assertTrue(user.is_authenticated)


class LogoutTest(TestCase):
    def setUp(self):
        self.client.login(username='augie', password='abcde12345')

        self.response = self.client.get(reverse('logout'))
        self.home_url = reverse('home')

    def test_redirection_after_logout(self):
        """this scinario is double redirect
        logout -> home -> login
        so need to check status_code 302
        assertRedirects()'s default expecting status_code is 200"""
        self.assertRedirects(self.response, self.home_url, status_code=302, target_status_code=302)

    def test_no_context_after_redirect(self):
        """can't test user's is_authenticated
        cuz there's no context data after redirect
        i only check existance of context"""
        res = self.client.get(self.home_url)
        self.assertEqual(res.context, None)
