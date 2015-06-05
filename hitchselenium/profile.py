from selenium import webdriver
import os


class Profile(webdriver.FirefoxProfile):
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        package_dir = os.path.abspath(os.path.dirname(__file__))
        self.add_extension(package_dir + os.sep + "selenium-ide.xpi")
        self.add_extension(package_dir + os.sep + "pythonformatters@seleniumhq.org.xpi")
        self.set_preference("extensions.selenium-ide.currentVersion", "2.5.0")
        self.set_preference("extensions.selenium-ide.enableExperimentalFeatures", "true")
        self.set_preference("extensions.selenium-ide.showDeveloperTools", "false")
        self.set_preference("extensions.selenium-ide.formats.pythonwdformatter.header", "")
        self.set_preference("extensions.selenium-ide.formats.pythonwdformatter.footer", "")
        self.set_preference("extensions.selenium-ide.selectedFormat", "pythonwdformatter")
