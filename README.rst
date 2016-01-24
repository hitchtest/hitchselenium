HitchSelenium
=============

HitchSelenium is a plugin for the Hitch testing framework that wraps selenium and
starts firefox, optionally with XVFB so the browser window does not appear.

Use with Hitch
==============

Install like so::

    $ hitch install hitchselenium


.. code-block:: python

        # Service definition in engine's setUp:
        self.services['Firefox'] = hitchselenium.SeleniumService(
            xvfb=False           # Optional (default: False)
        )

        # N.B. if xvfb is installed and xvfb is set to True, firefox will run hidden.

        # Open page and type something into text box with id id_description:
        self.driver = self.services['Firefox'].driver
        self.driver.get(self.url)
        self.driver.find_element_by_id("id_description").send_keys("type something...")

See this service in action at the DjangoRemindMe_ project.


Features
========

* Starts up the browser on a separate thread when running with HitchServe_, in parallel with starting other services, so that your integration tests run faster.
* You can optionally run the Firefox browser visibly and invisibly using XVFB.

Caveats
=======

* Currently only supports firefox.
* Might not necessarily work with the latest version of firefox.
* Faketime is not enabled since firefox does not respond well to it. Javascript will always return system time.

TODO
====

Download and install specified versions of firefox/chromium in .hitchpkg directory for all versions.


.. _HitchServe: https://github.com/hitchtest/hitchserve
.. _DjangoRemindMe: https://github.com/hitchtest/django-remindme
