from selenium import webdriver
from profile import Profile
import os
import json
import sys
import time


def run():
    driver = webdriver.Firefox(firefox_profile=Profile())
    #driver = webdriver.PhantomJS()
    sys.stdout.write("READY\n")
    sys.stdout.flush()
    config = {"uri": "http://127.0.0.1:{}/hub".format(driver.profile.port), }
    sys.stdout.write("{}\n".format(json.dumps(config)))
    sys.stdout.flush()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        driver.quit()
        sys.stdout.write("Firefox closed\n")
        sys.stdout.flush()

if __name__=='__main__':
    run()
