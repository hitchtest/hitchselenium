from selenium.webdriver.common.by import By
from hitchselenium import exceptions
import strictyaml


class CSSSelector(object):
    def __init__(self, code):
        self._code = code

    def find_element(self, driver):
        results = driver.find_elements_by_css_selector(self._code)
        if len(results) > 1:
            raise exceptions.SingleElementSelectorMatchedMoreElements(
                """{} elements were found matching CSS selector '{}'""".format(
                    len(results),
                    self._code,
                )
            )
        elif len(results) == 0:
            raise exceptions.SingleElementSelectorMatchedNoElements(
                """No element found matching CSS selector '{}'""".format(
                    self._code,
                )
            )
        else:
            return results[0]

    def conditions(self):
        return (By.CSS_SELECTOR, self._code)


class XPathSelector(object):
    def __init__(self, code):
        self._code = code

    def find_element(self, driver):
        results = driver.find_elements_by_xpath(self._code)
        if len(results) > 1:
            raise exceptions.SingleElementSelectorMatchedMoreElements(
                """{} elements were found matching XPath selector '{}'""".format(
                    len(results),
                    self._code,
                )
            )
        elif len(results) == 0:
            raise exceptions.SingleElementSelectorMatchedNoElements(
                """No element found matching XPath selector '{}'""".format(
                    self._code,
                )
            )
        else:
            return results[0]

    def conditions(self):
        return (By.XPATH, self._code)


class ReadableSelectorTranslator(object):
    def __init__(self, override_selectors=None):
        self._override_selectors = override_selectors

    def default(self, name):
        return CSSSelector("#{0}".format(name.replace(" ", "-")))

    def __call__(self, name):
        if self._override_selectors is not None:
            with open(self._override_selectors) as handle:
                selectors = strictyaml.load(handle.read())

            if name in selectors.keys():
                selector = selectors[name]

                if isinstance(selector, str):
                    return CSSSelector(selectors[name])
                else:
                    if "xpath" in selector.keys():
                        return XPathSelector(selector['xpath'])
        return self.default(name)
