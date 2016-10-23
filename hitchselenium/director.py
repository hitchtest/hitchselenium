from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from hitchselenium import exceptions
import time


class IndividualElement(object):
    def __init__(self, director, selector):
        self._director = director
        self._selector = selector

    @property
    def selector(self):
        return self._selector

    @property
    def director(self):
        return self._director

    def fill_text(self, text):
        """
        Fill text in a text box.

        Clears the text box of text first.
        """
        self.selector.find_element(self.director.driver).clear()
        self.selector.find_element(self.director.driver).send_keys(text)

    def send_keys(self, text):
        """
        Send specified keys to an element (dropdown, text box, etc.).

        Unlike fill_text, this method does not attempt to clear the element (i.e. text box) first.
        """
        self.selector.find_element(self.director.driver).send_keys(text)

    def click(self):
        """
        Click on element.
        """
        self.selector.find_element(self.director.driver).click()

    def should_appear(self):
        """
        Check that element is visible.
        """
        WebDriverWait(self.director.driver, self.director.default_timeout).until(
            expected_conditions.visibility_of_element_located(
                self.selector.conditions()
            )
        )

    def should_contain(self, text):
        """
        Check that text appears in element.
        """
        WebDriverWait(self.director.driver, self.director.default_timeout).until(
            expected_conditions.text_to_be_present_in_element(
                self.selector.conditions(), text
            )
        )



class PageUrl(object):
    def __init__(self, director):
        self._director = director


    def should_contain(self, text):
        wait_for = self._director.default_timeout
        for i in range(0, 10 * wait_for):
            if text in self._director.driver.current_url:
                return
            time.sleep(0.1)

        current_url = self._director.driver.current_url
        if text in current_url:
            return
        raise exceptions.ShouldHaveButDidNot(
            "URL '{}' did not contain '{}' after {} seconds.".format(
                current_url,
                text,
                wait_for,
            )
        )


class Director(object):
    def __init__(self, driver, selector_translator, default_timeout=5):
        self._driver = driver
        self._selector_translator = selector_translator
        self._default_timeout = default_timeout

    @property
    def default_timeout(self):
        return self._default_timeout

    @property
    def driver(self):
        return self._driver

    def visit(self, url):
        """
        Load URL.
        """
        self.driver.get(url)

    @property
    def url(self):
        return PageUrl(self)

    def the(self, identifier):
        return IndividualElement(self, self._selector_translator(identifier))
