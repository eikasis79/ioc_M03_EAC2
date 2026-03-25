from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class MySeleniumTests(StaticLiveServerTestCase):
    # no crearem una BD de test en aquesta ocasió (comentem la línia)
    # fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # creem usuari staff
        user = User.objects.create_user("gerard", "gerard@isardvdi.com", "gerard")
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # login al panell d'admin
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('gerard')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('gerard')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

        # anar directament a la pàgina de canvi de contrasenya
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/password_change/'))

        # canviar contrasenya
        self.selenium.find_element(By.NAME, "old_password").send_keys("gerard")
        self.selenium.find_element(By.NAME, "new_password1").send_keys("pirineus")
        self.selenium.find_element(By.NAME, "new_password2").send_keys("pirineus")
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()

        # logout fent click al botó del formulari
        self.selenium.find_element(
            By.XPATH,
            '//form[@id="logout-form"]//button[@type="submit"]'
        ).click()

        # clicar "Log in again"
        self.selenium.find_element(By.LINK_TEXT, "Log in again").click()

        # login amb la nova contrasenya
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('gerard')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        # comprovació final
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")