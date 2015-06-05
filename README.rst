HitchSelenium
=============

HitchSelenium is a plugin for the Hitch testing framework that wraps selenium.

Use with Hitch
==============

Install like so::

    $ hitch install hitchselenium


.. code-block:: python

        # Service definition in setup.py's setUp:
        self.services['Firefox'] = services.SeleniumService(xvfb=False) # xvfb = True hides the firefox UI

        # Open page and type something into text box with id id_description:
        self.driver = self.services['Firefox'].driver
        self.driver.get(self.url)
        self.driver.find_element_by_id("id_description").send_keys(description)

See this service in action at the DjangoRemindMe_ project.


Features
========

* Starts up the browser on a separate thread when running with HitchServe_, in parallel, so that your integration tests run faster.
* You can optionally run the Firefox browser visibly and invisibly using XVFB.
* Comes pre-installed with Selenium IDE firefox plugin so you can record clicks and generate python code.


Caveats
=======

* Currently only supports firefox.


.. _HitchServe: https://github.com/crdoconnor/hitchserve
