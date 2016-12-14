from selenium import webdriver


class Profile(webdriver.FirefoxProfile):
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.set_preference("browser.startup.homepage_override.mstone", "ignore")
        self.set_preference("startup.homepage_welcome_url.additional", "about:blank")
        self.set_preference("browser.shell.checkDefaultBrowser", False)
        self.set_preference("devtools.webconsole.persistlog", True)
        self.set_preference("app.update.enabled", False)
