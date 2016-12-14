from hitchtest.environment import checks
from hitchserve import Service
from selenium import webdriver
import hitchselenium
import json
import sys


class FirefoxService(Service):
    """Firefox with selenium as a service."""

    def __init__(
        self,
        firefox_binary,
        xvfb=False,
        shunt_window=True,
        implicitly_wait=5.0,
        preferences=None,
        **kwargs
    ):
        """Initialize selenium Service object (but don't run).

        Args:
            xvfb (Optional[bool]): Run service with X virtual framebuffer
                (don't show firefox window).
            shunt_window (Optional[bool]): Shunt window to (0, 0) coordinates
                (move out of the way of the mouse)
            implicitly_wait (Optional[float]): Set implicitly_wait value of the selenium driver.
                (Default: 5.0 seconds.)
        """

        checks.packages(hitchselenium.UNIXPACKAGES)

        if xvfb:
            if sys.platform == "darwin":
                raise RuntimeError("Hitch can't use xvfb on Mac OS X")
        else:
            # If it's Linux and we're not using xvfb, we need X available
            if sys.platform != "darwin":
                checks.x_available(True)

        kwargs['log_line_ready_checker'] = lambda line: "READY" in line
        xvfb_run = ['xvfb-run'] if xvfb else []
        kwargs['command'] = xvfb_run + [
            sys.executable,
            "-u",
            "-m", "hitchselenium.server",
            str(firefox_binary),
            json.dumps(preferences) if preferences else json.dumps([])
        ]
        kwargs['no_libfaketime'] = True
        self.shunt_window = shunt_window
        self.implicitly_wait = implicitly_wait
        self._driver = None
        super(FirefoxService, self).__init__(**kwargs)

    @property
    def driver(self):
        """Get selenium driver object."""
        if self._driver is not None:
            return self._driver
        else:
            self._driver = webdriver.Remote(
                command_executor=self.logs.json()[0]['uri'],
                desired_capabilities={}
            )
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
            return super(FirefoxService, self).env_vars
