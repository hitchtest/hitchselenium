class HitchSeleniumException(Exception):
    pass


class SingleElementSelectorMatchedMoreElements(HitchSeleniumException):
    pass


class SingleElementSelectorMatchedNoElements(HitchSeleniumException):
    pass


class ShouldHaveButDidNot(HitchSeleniumException):
    pass
