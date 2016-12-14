from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from hitchselenium.profile import Profile
from selenium import webdriver
from sys import stdout, stderr
import json
import time
import sys
import os


def stop(driver):
    driver.quit()
    stdout.write("Firefox closed\n")
    stdout.flush()


def runserver():
    if "DISPLAY" not in os.environ and sys.platform != "darwin":
        stderr.write(
            "The DISPLAY environment variable is not set.\n"
            "This usually means that X is not available.\n"
            "Information on how to fix this problem can be found here:\n"
            "https://stackoverflow.com/questions/784404/how-can-i-specify-a-display\n"
        )

    profile = Profile()

    for preference in json.loads(sys.argv[2]):
        profile.set_preference(list(preference.keys())[0], list(preference.values())[0])

    driver = webdriver.Firefox(
        firefox_profile=profile,
        firefox_binary=FirefoxBinary(firefox_path=sys.argv[1], log_file=sys.stdout)
    )
    config = {"uri": "http://127.0.0.1:{}/hub".format(driver.profile.port), }
    stdout.write("{}\n".format(json.dumps(config)))
    stdout.flush()
    stdout.write("READY\n")
    stdout.flush()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop(driver)
    except SystemExit:
        stop(driver)


if __name__ == '__main__':
    runserver()
