import unittest

import selenium
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


class CamacTestUtils(unittest.TestCase):
    _URL = 'http://localhost:4300'

    def setUp(self):
        self.browser = selenium.webdriver.Firefox()

    def login(self, username, password):
        self.browser.get(self._URL)
        elem_user = self.browser.find_element_by_name('username')
        elem_pass = self.browser.find_element_by_name('password')

        elem_user.send_keys(username)
        elem_pass.send_keys(password)

        elem_pass.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'nav-level-1'))
        )

    def create_form_43(self):
        self.browser.get(self._URL + '/form/new/instance-resource-id/' +
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

    def create_form_44(self):
        self.browser.get(self._URL + '/form/new/instance-resource-id/' +
                         '1/instance-id/-1/form-id/44')

        create_b = self.browser.find_element_by_id('button_2')
        create_b.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'c2q1i1'))
        )

        self.instance_id = int(self.browser.current_url.split('/')[-1])

    def tearDown(self):
        self.browser.quit()
