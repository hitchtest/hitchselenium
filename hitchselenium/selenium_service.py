from hitchserve import Service
from selenium import webdriver
import sys
import os


class SeleniumService(Service):

    def __init__(self, xvfb=False, shunt_window=True, **kwargs):
        kwargs['log_line_ready_checker'] = lambda line: "READY" in line
        xvfb_run = ['xvfb-run'] if xvfb else []
        kwargs['command'] = xvfb_run + [sys.executable, "-u", "-m", "hitchselenium.server"]
        self.shunt_window = shunt_window
        self._driver = None
        super(SeleniumService, self).__init__(**kwargs)

    @property
    def driver(self):
        if self._driver is not None:
            return self._driver
        else:
            self._driver = webdriver.Remote(command_executor=self.logs.json()[0]['uri'], desired_capabilities={})
            self._driver.implicitly_wait(5.0)
            self._driver.accept_next_alert = True
            return self._driver

    def poststart(self):
        """Move the firefox window out of the way of the mouse."""
        if self.shunt_window:
            driver = self.driver
            driver.set_window_position(0, 0)

    @Service.env_vars.getter
    def env_vars(self):
        if sys.platform == "darwin":
            return {}
        else:
            return super(SeleniumService, self).env_vars
