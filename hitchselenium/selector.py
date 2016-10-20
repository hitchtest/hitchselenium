from selenium.webdriver.common.by import By
import strictyaml


class CSSSelector(object):
    def __init__(self, code):
        self._code = code

    def find_element(self, driver):
        return driver.find_element_by_css_selector(self._code)

    def conditions(self):
        return (By.CSS_SELECTOR, self._code)


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
                return CSSSelector(selectors[name])
        return self.default(name)
