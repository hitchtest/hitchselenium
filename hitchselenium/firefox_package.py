from hitchtest import HitchPackage, utils
from hitchtest.executionengine import Paths
from subprocess import check_output, check_call
from os.path import join, exists
from os import makedirs
from hitchselenium import exceptions
import shutil
import struct
import sys


ISSUES_URL = "http://github.com/hitchtest/hitchselenium/issues"

RELEASE_URL_BASE = "https://download-installer.cdn.mozilla.net/pub/firefox/releases/"


class FirefoxPackage(HitchPackage):
    VERSIONS = [
        "46.0.1",
    ]

    name = "Firefox"

    def __init__(self, version="46.0.1", paths=None, directory=None):
        super(FirefoxPackage, self).__init__()
        self.version = self.check_version(version, self.VERSIONS, ISSUES_URL)
        if paths is None:
            paths = Paths()
            self._firefox_path = join(
                self.get_downloads_directory(),
                "firefox-{}".format(version)
            )
        else:
            self._firefox_path = paths.hitchpkg.joinpath(
                "firefox-{0}".format(version=self.version)
            ).abspath()

        self.directory = self._firefox_path
        self.tmp_directory = '/tmp/firefoxmount'

    def verify(self):
        version_output = check_output([self.firefox, "--version"]).decode('utf8')
        if self.version not in version_output:
            raise exceptions.WrongFirefoxVersion(
                "Firefox version needed is {0}, output is: {1}.".format(
                    self.version, version_output
                )
            )

    def build(self):
        if sys.platform == "darwin":
            download_to = join(
                self.get_downloads_directory(),
                "firefox-{}.dmg".format(self.version)
            )
            self.download_url = "{0}{1}/mac/en-US/Firefox%20{1}.dmg".format(
                RELEASE_URL_BASE,
                self.version
            )
        else:
            download_to = join(
                self.get_downloads_directory(),
                "firefox-{}.tar.gz".format(self.version)
            )
            systembits = struct.calcsize("P") * 8

            if systembits == 32:
                self.download_url = "{0}{1}/linux-i686/en-US/firefox-{1}.tar.bz2".format(
                    RELEASE_URL_BASE, self.version
                )
            else:
                self.download_url = "{0}{1}/linux-x86_64/en-US/firefox-{1}.tar.bz2".format(
                    RELEASE_URL_BASE, self.version
                )
        utils.download_file(download_to, self.download_url)

        if sys.platform == "darwin":
            if not exists(self.directory):
                check_call([
                    "hdiutil", "attach", "-nobrowse", "-mountpoint",
                    self.tmp_directory, download_to
                ])
                makedirs(join(self.directory, "Firefox.app"))
                shutil.copytree(
                    join(self.tmp_directory, "Firefox.app", "Contents"),
                    join(self.directory, "Firefox.app", "Contents")
                )
                check_call(["hdiutil", "detach", self.tmp_directory])
            self.bin_directory = join(self.directory, "Firefox.app", "Contents", "MacOS")
        else:
            if not exists(self.directory):
                makedirs(self.directory)
                utils.extract_archive(download_to, self.directory)
            self.bin_directory = join(self.directory, "firefox")
        self.verify()

    @property
    def firefox(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        if sys.platform == "darwin":
            return join(self.bin_directory, "firefox-bin")
        else:
            return join(self.bin_directory, "firefox")
