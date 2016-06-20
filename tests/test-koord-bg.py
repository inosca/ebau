import unittest
import selenium
import selenium.webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


URL = 'http://localhost:4300'

username = 'stefanheinemann'
password = 'camac'


class CamacTestUtils(unittest.TestCase):
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

    def tearDown(self):
        self.browser.quit()


class TestLogin(CamacTestUtils):

    def setUp(self):
        self.browser = selenium.webdriver.Firefox()

    def test_site_reachable(self):
        self.browser.get(URL)

        self.assertNotEqual(self.browser.title, '')

    def test_login(self):
        self.login()

    def test_all_nav_items_present(self):
        self.login()
        self.assertEqual(5, len(self.browser.find_elements_by_css_selector(
            '.nav-level-1 li')))


class TestCreateDossier(CamacTestUtils):
    def test_creation_list(self):
        self.login()
        self.browser.get(URL + '/index/index/resource-id/22')
        links = self.browser.find_elements_by_css_selector('.links a')

        self.assertEqual(5, len(links))

    def test_dossier_cration_form(self):
        self.login()
        self.browser.get(URL +
                         '/form/new/instance-resource-id/106/' +
                         'instance-id/-1/form-id/43')

        communities = self.browser.find_elements_by_css_selector(
            '#c3q2i1 option')

        self.assertEqual(21, len(communities))

        authorities = self.browser.find_elements_by_css_selector(
            '#c3q5i1 option')

        self.assertEqual(51, len(authorities))


class TestDossierRelated(CamacTestUtils):

    def create_form_43(self):
        self.login()
        self.browser.get(URL + '/form/new/instance-resource-id/' +
                         '106/instance-id/-1/form-id/43')

        com = Select(self.browser.find_element_by_id('c3q2i1'))
        com.select_by_visible_text("Altdorf")

        auth = Select(self.browser.find_element_by_id('c3q5i1'))
        auth.select_by_visible_text("Amt für Energie")

        create_b = self.browser.find_element_by_id('button_64')
        create_b.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'c2q1i1'))
        )

        self.instance_id = int(self.browser.current_url.split('/')[-1])


class TestDossierFinish(TestDossierRelated):

    def test_docgen(self):
        self.create_form_43()

        self.browser.get(URL + '/circulation/index/' +
                         'instance-resource-id/314/instance-id/%i' %
                         self.instance_id)

        letter_b = self.browser.find_element_by_id('button_288')
        letter_b.click()




if __name__ == '__main__':
    unittest.main()
