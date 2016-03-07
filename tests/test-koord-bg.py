import unittest
import selenium
import selenium.webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'http://localhost:4300'

username = 'tester'
password = '123qwe'


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.browser = selenium.webdriver.Firefox()

    def login(self):
        self.browser.get(URL)
        elem_user = self.browser.find_element_by_name('username')
        elem_pass = self.browser.find_element_by_name('password')

        elem_user.send_keys(username)
        elem_pass.send_keys(password)

        elem_pass.send_keys(Keys.RETURN)

    def test_site_reachable(self):
        self.browser.get(URL)

        self.assertNotEqual(self.browser.title, '')

    def test_login(self):
        self.login()

    def test_all_nav_items_present(self):
        self.login()
        self.assertEquals(5, len(self.browser.find_elements_by_css_selector(
            '.nav-level-1 li')))

    def tearDown(self):
        self.browser.quit()


class TestCreateDossier(unittest.TestCase):

    def setUp(self):
        self.browser = selenium.webdriver.Firefox()
        self.login()

    def login(self):
        self.browser.get(URL)
        elem_user = self.browser.find_element_by_name('username')
        elem_pass = self.browser.find_element_by_name('password')

        elem_user.send_keys(username)
        elem_pass.send_keys(password)

        elem_pass.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'nav-level-1'))
        )

    def test_creation_list(self):
        self.login()
        self.browser.get(URL + '/index/index/resource-id/22')
        links = self.browser.find_elements_by_css_selector('.links a')

        self.assertEqual(5, len(links))

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main()
