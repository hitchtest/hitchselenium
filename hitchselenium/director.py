from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from hitchselenium import exceptions
import time
import re


class Expectation(object):
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element = expected_conditions._find_element(driver, self.locator)
            return self.check(element)
        except exceptions.StaleElementReferenceException:
            return False


class text_to_be_equal_in_element_contents_or_value(Expectation):
    """
    An expectation for checking if the given text is equal in the
    specified element or its value attribute.
    """
    def check(self, element):
        return self.text == element.text or self.text == element.get_attribute("value")


class text_to_be_present_in_element_contents_or_value(Expectation):
    """
    An expectation for checking if the given text is present in the element's
    text or its value attribute.
    """
    def check(self, element):
        return self.text in element.text or self.text in element.get_attribute("value")


class regex_to_be_present_in_element_contents_or_value(Expectation):
    """
    An expectation for checking if the given regex is found in the element's
    text or its value attribute.
    """
    def check(self, element):
        return self.text.search(element.text) is not None or self.text.search(element.get_attribute("value")) is not None


class regex_to_be_equal_in_element_contents_or_value(Expectation):
    """
    An expectation for checking if the given regex *matches* the element's
    text or its value attribute.
    """
    def check(self, element):
        return self.text.match(element.text) is not None or self.text.match(element.get_attribute("value")) is not None



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
        Wait for element to appear; throw exception if it does not.
        """
        WebDriverWait(self.director.driver, self.director.default_timeout).until(
            expected_conditions.visibility_of_element_located(
                self.selector.conditions()
            )
        )

    def should_contain(self, text):
        """
        Wait for element to contain text somewhere in it; throw exception if it does not.

        Checks contents of tags (e.g. <span>contents</span>) and elements
        with values (e.g. <input name="textbox" value="contents" />).

        text can be a string or a python regular expression object.
        """
        assert type(text) is str or type(text) is type(re.compile(""))

        if type(text) is str:
            WebDriverWait(self.director.driver, self.director.default_timeout).until(
                text_to_be_present_in_element_contents_or_value(
                    self.selector.conditions(), text
                )
            )
        else:
            WebDriverWait(self.director.driver, self.director.default_timeout).until(
                regex_to_be_present_in_element_contents_or_value(
                    self.selector.conditions(), text
                )
            )

    def should_only_contain(self, text):
        """
        Wait for element to contain exact text; throw exception if it does not.

        Checks contents of tags (e.g. <span>contents</span>) and elements
        with values (e.g. <input name="textbox" value="contents" />).
        """
        if type(text) is str:
            WebDriverWait(self.director.driver, self.director.default_timeout).until(
                text_to_be_equal_in_element_contents_or_value(
                    self.selector.conditions(), text
                )
            )
        else:
            WebDriverWait(self.director.driver, self.director.default_timeout).until(
                regex_to_be_equal_in_element_contents_or_value(
                    self.selector.conditions(), text
                )
            )

    def contents(self):
        """
        Get text contents of any label.
        """
        return self.selector.find_element(self.director.driver).text



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
