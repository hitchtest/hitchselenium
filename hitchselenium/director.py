from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Director(object):
    def __init__(self, driver, default_timeout=5):
        self._driver = driver
        self._timeout = default_timeout

    @property
    def driver(self):
        return self._driver

    def click(self, selector):
        selector.find_element(self.driver).click()

    def appear(self, selector):
        WebDriverWait(self.driver, self._timeout).until(
            expected_conditions.visibility_of_element_located(
                selector.conditions()
            )
        )

    def visit(self, url):
        self.driver.get(url)