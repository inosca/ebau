import unittest

import selenium
import selenium.webdriver
from testutils import CamacTestUtils

URL = 'http://localhost:4300'

logins = {
    'koor': {
        'username': 'stefanheinemann',
        'password': 'camac'
    },
    'community': {
        'username': 'Altdorf1',
        'password': 'camac'
    }
}


class TestUploadDropdowns(CamacTestUtils):

    def test_koor_selects(self):
        self.login(logins['koor']['username'], logins['koor']['password'])
        self.create_form_43()

        URL = "/".join([
            self._URL,
            '/documents/list/list/instance-resource-id/145/instance-id',
            str(self.instance_id)
        ])

        self.browser.get(URL)

        dropdown = self.browser.find_element_by_id('upload_as')
        self.assertIsInstance(dropdown,
                              selenium.webdriver.remote.webelement.WebElement)

    def test_community_selects(self):
        login = logins['community']
        self.login(login['username'], login['password'])
        self.create_form_44()

        URL = "/".join([
            self._URL,
            '/documents/list/list/instance-resource-id/46/instance-id',
            str(self.instance_id)
        ])

        self.browser.get(URL)

        self.assertRaises(
            selenium.common.exceptions.NoSuchElementException,
            lambda : self.browser.find_element_by_id('upload_as')
        )

if __name__ == '__main__':
    unittest.main()
