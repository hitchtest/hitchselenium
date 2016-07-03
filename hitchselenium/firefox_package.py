from hitchtest import HitchPackage, utils
from hitchtest.environment import checks
from subprocess import check_output, call, check_call
from os.path import join, exists
from os import makedirs, chdir, environ
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import hitchselenium
import struct
import sys


ISSUES_URL = "http://github.com/hitchtest/hitchselenium/issues"

class FirefoxPackage(HitchPackage):
    VERSIONS = [
        "46.0.1",
    ]

    name = "Firefox"

    def __init__(self, version="46.0.1", directory=None, bin_directory=None):
        super(FirefoxPackage, self).__init__()
        self.version = self.check_version(version, self.VERSIONS, ISSUES_URL)
        self.subdirectory = "firefox"

        if directory is None:
            if sys.platform == "darwin":
                self.download_url = "https://download-installer.cdn.mozilla.net/pub/firefox/releases/{0}/mac/en-US/Firefox%20{0}.dmg".format(self.version)
            else:
                systembits = struct.calcsize("P") * 8

                if systembits == 32:
                    self.download_url = "https://download-installer.cdn.mozilla.net/pub/firefox/releases/{0}/linux-i686/en-US/firefox-{0}.tar.bz2".format(self.version)
                else:
                    self.download_url = "https://download-installer.cdn.mozilla.net/pub/firefox/releases/{0}/linux-x86_64/en-US/firefox-{0}.tar.bz2".format(self.version)
            self.directory = join(self.get_build_directory(), "firefox-{}".format(self.version), "firefox")
        else:
            self.directory = directory

        #checks.packages(hitchselenium.UNIXPACKAGES)

    def verify(self):
        version_output = check_output([self.firefox, "--version"]).decode('utf8')
        if self.version not in version_output:
            raise RuntimeError("Firefox version needed is {}, output is: {}.".format(self.version, version_output))

    def build(self):
        download_to = join(self.get_downloads_directory(), "firefox-{}.tar.gz".format(self.version))
        utils.download_file(download_to, self.download_url)

        if not exists(self.directory):
            makedirs(self.directory)
            utils.extract_archive(download_to, self.directory)
        self.bin_directory = join(self.directory, "firefox")
        self.verify()

    @property
    def firefox(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "firefox")