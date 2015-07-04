from selenium import webdriver
import os


class Profile(webdriver.FirefoxProfile):
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
