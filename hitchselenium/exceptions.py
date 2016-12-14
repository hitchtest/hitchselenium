class HitchSeleniumException(Exception):
    pass


class SingleElementSelectorMatchedMoreElements(HitchSeleniumException):
    pass


class SingleElementSelectorMatchedNoElements(HitchSeleniumException):
    pass


class ShouldHaveButDidNot(HitchSeleniumException):
    pass


class PageScreenshotDifferent(HitchSeleniumException):
    pass


class WrongFirefoxVersion(HitchSeleniumException):
    pass
