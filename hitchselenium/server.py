from hitchselenium.profile import Profile
from selenium import webdriver
from sys import stdout
import json
import time


def stop():
    driver.quit()
    stdout.write("Firefox closed\n")
    stdout.flush()

def run():
    driver = webdriver.Firefox(firefox_profile=Profile())
    stdout.write("READY\n")
    stdout.flush()
    config = {"uri": "http://127.0.0.1:{}/hub".format(driver.profile.port), }
    stdout.write("{}\n".format(json.dumps(config)))
    stdout.flush()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop()
    except SystemExit:
        stop()

if __name__=='__main__':
    run()
