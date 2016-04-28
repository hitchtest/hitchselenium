import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from os.path import join, abspath, exists
import selenium
import re
import os


class HitchSeleniumException(Exception):
    pass


class BadItemDescription(HitchSeleniumException):
    def __init__(self, begin, item):
        super(BadItemDescription, self).__init__((
            "'{}' in '{}' should be either first, 2nd, 3rd, 4th, etc. or last"
        ).format(begin, item))


class HitchUploadFileNotFound(HitchSeleniumException):
    def __init__(self, path):
        super(HitchUploadFileNotFound, self).__init__((
            "'{}' not found. Check upload_directory in the SeleniumStepLibrary is correct?"
        ).format(path))


class HitchSeleniumItem(object):
    """Representation of an HTML 'hitch item' selector. If the selector
       contains no spaces, it is assumed to be an HTML id.

       If the selector contains spaces, it is assumed to be of the form:

         * first htmlclass1 htmlclass2
         * 2nd htmlclass1 htmlclass2
         * 3rd htmlclass1 htmlclass2
         etc.
    """
    def __init__(self, item):
        self._item = item
        self._html_classes = None
        self._index = None
        if not self.is_id:
            sequence = item.split(" ")
            begin = sequence[0].lower()
            number_from_begin = re.sub(r'[^0-9]', "", begin)
            self._html_classes = sequence[1:]
            if begin == "first":
                self._index = 0
            elif begin == "last":
                self._index = -1
            elif number_from_begin == "":
                raise BadItemDescription(begin, item)
            else:
                self._index = int(number_from_begin) - 1

    @property
    def index(self):
        return self._index

    @property
    def html_classes(self):
        return self._html_classes

    @property
    def is_id(self):
        return " " not in self._item

    @property
    def html_id(self):
        if self.is_id:
            return self._item
        else:
            raise RuntimeError("'{}' is not an HTML id".format(self._item))



class SeleniumStepLibrary(object):
    """A package of steps which can be used to test command line applications."""

    def __init__(self, selenium_webdriver, wait_for_timeout=5, upload_directory=os.getcwd()):
        """Create a library of steps using a selenium webdriver.

           selenium_webdriver - webdriver object.
           wait_for_timeout - number of seconds to wait during "wait steps".
        """
        self.driver = selenium_webdriver
        self.wait_for_timeout = wait_for_timeout
        self.upload_directory = upload_directory

    def click(self, item):
        """Click on item.

           * If there are no spaces, clicks on element with HTML id "item".
           * "first class1" - clicks on first element with the HTML class "class1"
           * "2nd class1 class2" - clicks on the second element with HTML classes class1 and class2.
           * "last class1 class2" - clicks on the last element with classes class1 and class2
        """
        item = HitchSeleniumItem(item)
        if item.is_id:
            self.driver.find_element_by_id(item.html_id).click()
        else:
            self.driver.find_elements_by_css_selector(
                "." + ".".join(item.html_classes)
            )[item.index].click()


    def enter_text(self, item=None, text=None):
        """Enter text to a specified element.

           * If there are no spaces, clicks on element with HTML id "item".
           * "first class1" - clicks on first element with the HTML class "class1"
           * "2nd class1 class2" - clicks on the second element with HTML classes class1 and class2.
           * "last class1 class2" - clicks on the last element with classes class1 and class2
        """
        item = HitchSeleniumItem(item)
        if item.is_id:
            element = self.driver.find_element_by_id(item.html_id)
        else:
            element = self.driver.find_elements_by_css_selector(
                "." + ".".join(item.html_classes)
            )[item.index]
        element.clear()
        element.send_keys(text)


    def upload_file(self, item=None, path=None):
        """Upload file name relative to upload_directory set in constructor.

           * If there are no spaces, clicks on element with HTML id "item".
           * "first class1" - clicks on first element with the HTML class "class1"
           * "2nd class1 class2" - clicks on the second element with HTML classes class1 and class2.
           * "last class1 class2" - clicks on the last element with classes class1 and class2
        """
        full_path = abspath(join(self.upload_directory, path))

        if not exists(full_path):
            raise HitchUploadFileNotFound(full_path)
        
        item = HitchSeleniumItem(item)
        if item.is_id:
            self.driver.find_element_by_id(item.html_id).send_keys(full_path)
        else:
            self.driver.find_elements_by_css_selector(
                "." + ".".join(item.html_classes)
            )[item.index].send_keys(full_path)


    def wait_to_appear(self, item):
        """Wait for item to appear

           * If there are no spaces in item, waits for element with HTML id "item" to appear.
           * "first class1" - waits for first item with  HTML class "class1" to appear.
           * "2nd class1 class2" - waits for the 2nd item with HTML classes class1 and class2 to appear.
           * "last class1 class2" - waits for the last element with classes class1 and class2 to appear.
        """
        item = HitchSeleniumItem(item)
        if item.is_id:
            WebDriverWait(self.driver, self.wait_for_timeout).until(
                EC.visibility_of_element_located((By.ID, item.html_id))
            )
        else:
            full_xpath = """//*[{}][{}]""".format(
                " and ".join([
                    """contains(concat(' ', normalize-space(@class), ' '), ' {} ')""".format(
                        class_name
                    ) for class_name in item.html_classes]
                ),
                str(item.index + 1) if item.index >= 0 else "last()"
            )

            WebDriverWait(self.driver, self.wait_for_timeout).until(
                EC.visibility_of_element_located((By.XPATH, full_xpath))
            )

    def should_not_appear(self, item):
        """Wait and make sure an item does NOT appear.

           Note that this makes use of 'wait_to_appear', and so if the item
           in question takes longer to appear than wait_to_appear takes to
           time out then it will be considered not to have appeared.

           * If there are no spaces in item, waits for element with HTML id
             "item" to appear.
           * "first class1" - waits for first item with  HTML class "class1"
             to appear.
           * "2nd class1 class2" - waits for the 2nd item with HTML classes
             class1 and class2 to appear.
           * "last class1 class2" - waits for the last element with classes
             class1 and class2 to appear.
        """
        try:
            self.wait_to_appear(item)
            raise RuntimeError(
                "Item {} should not have appeared".format(item)
            )
        except TimeoutException:
            pass

    def wait_for_form_item_to_contain(self, item=None, text=None):
        item = HitchSeleniumItem(item)
        if item.is_id:
            WebDriverWait(self.driver, self.wait_for_timeout).until(
                EC.text_to_be_present_in_element_value((By.ID, item.html_id), text)
            )
        else:
            full_xpath = """//*[{}][{}]""".format(
                " and ".join([
                    """contains(concat(' ', normalize-space(@class), ' '), ' {} ')""".format(
                        class_name
                    ) for class_name in item.html_classes]
                ),
                str(item.index + 1) if item.index >= 0 else "last()"
            )

            WebDriverWait(self.driver, self.wait_for_timeout).until(
                EC.text_to_be_present_in_element_value(
                    (By.XPATH, full_xpath), text
                )
            )


    def wait_to_contain(self, item=None, text=None):
        """Wait for item like a label to contain text.

           * If there are no spaces in item, waits for element with HTML id "item" to contain 'text'
           * "first class1" - waits for first item with  HTML class "class1" to contain text.
           * "2nd class1 class2" - waits for the 2nd item with HTML classes class1 and class2 to contain 'text'.
           * "last class1 class2" - waits for the last element with classes class1 and class2 to contain 'text'.
        """
        item = HitchSeleniumItem(item)
        if item.is_id:
            WebDriverWait(self.driver, self.wait_for_timeout).until(
                EC.text_to_be_present_in_element((By.ID, item.html_id), text)
            )
        else:
            full_xpath = """//*[{}][{}]""".format(
                " and ".join([
                    """contains(concat(' ', normalize-space(@class), ' '), ' {} ')""".format(
                        class_name
                    ) for class_name in item.html_classes]
                ),
                str(item.index + 1) if item.index >= 0 else "last()"
            )

            WebDriverWait(self.driver, self.wait_for_timeout).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, full_xpath), text
                )
            )

    def wait_for_any_to_contain(self, items=None, text=None):
        """Wait for any of the non-form items to contain text.

           Where items is a space separated list of HTML classes."""
        full_xpath = """//*[{}][{}]""".format(
            " and ".join([
                """contains(concat(' ', normalize-space(@class), ' '), ' {} ')""".format(
                    class_name
                ) for class_name in items.split(" ")]
            ),
            "text()='{}'".format(text)
        )
        WebDriverWait(self.driver, self.wait_for_timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, full_xpath)
            )
        )

    def click_and_dont_wait_for_page_load(self, item):
        """Click on item but don't wait for page to load (useful for connecting to ipython kernel)

           * If there are no spaces, clicks on element with HTML id "item".
           * "first class1" - clicks on first element with the HTML class "class1"
           * "2nd class1 class2" - clicks on the second element with HTML classes class1 and class2.
           * "last class1 class2" - clicks on the last element with classes class1 and class2
        """
        item = HitchSeleniumItem(item)
        if item.is_id:
            self.driver.execute_script("document.getElementById('{}').click();".format(item.html_id))
        else:
            if item.index >= 0:
                self.driver.execute_script(
                    "document.getElementsByClassName('{}')[{}].click();".format(
                        " ".join(item.html_classes), item.index
                    )
                )
            else:
                self.driver.execute_script((
                    "collection=document.getElementsByClassName('{}'); "
                    "collection[collection.length-1].click();"
                ).format(" ".join(item.html_classes)))
