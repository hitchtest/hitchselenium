from hitchtest.environment import checks
from hitchserve import Service
from selenium import webdriver
import sys


class SeleniumService(Service):
    """Firefox with selenium as a service."""

    def __init__(self, xvfb=False, shunt_window=True, implicitly_wait=5.0, **kwargs):
        """Initialize selenium Service object (but don't run).

        Args:
            xvfb (Optional[bool]): Run service with X virtual framebuffer (don't show firefox window).
            shunt_window (Optional[bool]): Shunt window to (0, 0) coordinates to move out of the way of the mouse.
            implicitly_wait (Optional[float]): Set implicitly_wait value of the selenium driver. Default: 5.0 seconds.
        """

        checks.packages([
            "firefox", "xvfb", "xauth", "xserver-xorg", "dbus-x11", "ca-certificates"
        ])

        if not xvfb:
            if sys.platform != "darwin":
                checks.x_available(True)

        kwargs['log_line_ready_checker'] = lambda line: "READY" in line
        xvfb_run = ['xvfb-run'] if xvfb else []
        kwargs['command'] = xvfb_run + [sys.executable, "-u", "-m", "hitchselenium.server"]
        kwargs['no_libfaketime'] = True
        self.shunt_window = shunt_window
        self.implicitly_wait = implicitly_wait
        self._driver = None
        super(SeleniumService, self).__init__(**kwargs)

    @property
    def driver(self):
        """Get selenium driver object."""
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
