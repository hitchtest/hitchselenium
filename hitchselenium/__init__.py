from hitchselenium.step_library import SeleniumStepLibrary
from hitchselenium.selenium_service import SeleniumService
from hitchselenium.firefox_package import FirefoxPackage
from hitchselenium.profile import Profile
from hitchselenium.server import run


UNIXPACKAGES = [
    "xvfb", "xauth", "xserver-xorg", "dbus-x11", "ca-certificates",
]
