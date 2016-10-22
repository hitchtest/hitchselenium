from commandlib import run
import hitchselenium
import hitchpython
import hitchserve
import hitchtest
import hitchcli
import requests
import kaching
import time
import sys


class ExecutionEngine(hitchtest.ExecutionEngine):
    """Hitch bootstrap engine tester."""

    def set_up(self):
        self.path.project = self.path.engine.parent
        self.path.state = self.path.engine.parent.joinpath("state")
        self.path.samples = self.path.engine.joinpath("samples")

        if self.path.state.exists():
            self.path.state.rmtree()
        self.path.state.mkdir()

        if self.settings.get("kaching", False):
            kaching.start()

        self.python_package = hitchpython.PythonPackage(
            python_version=self.settings['python_version']
        )
        self.python_package.build()
        
        self.firefox_package = hitchselenium.FirefoxPackage()
        self.firefox_package.build()

        self.python = self.python_package.cmd.python
        self.pip = self.python_package.cmd.pip

        #self.cli = hitchcli.CommandLineStepLibrary(
            #default_timeout=int(self.settings.get("cli_timeout", 5))
        #)


        #self.cd = self.cli_steps.cd
        #self.run = self.cli_steps.run
        #self.expect = self.cli_steps.expect
        #self.send_control = self.cli_steps.send_control
        #self.send_line = self.cli_steps.send_line
        #self.exit_with_any_code = self.cli_steps.exit_with_any_code
        #self.exit = self.cli_steps.exit
        #self.finish = self.cli_steps.finish

        run(self.pip("uninstall", "hitchselenium", "-y").ignore_errors())
        run(self.pip("install", ".").in_dir(
            self.path.project.joinpath("..", "test")    # Install hitchtest
        ))
        run(self.pip("install", ".").in_dir(self.path.project))
        run(self.pip("install", "ipykernel"))
        run(self.pip("install", "pip"))
        run(self.pip("install", "q"))
        run(self.pip("install", "pudb"))

        self.path.state.joinpath("index.html").write_text(
            self.settings['html_base'].format(core=self.preconditions['html'])
        )
        
        if "selectors" in self.preconditions:
            self.path.state.joinpath("selectors.yaml").write_text(self.preconditions['selectors'])

        self.path.state.joinpath("success.html").write_text(self.settings['success_html'])

        self.cli = hitchcli.CommandLineStepLibrary(
            default_timeout=int(self.settings.get("cli_timeout", 720))
        )

        self.services = hitchserve.ServiceBundle(
            self.path.project,
            startup_timeout=8.0,
            shutdown_timeout=1.0
        )

        self.services['Webserver'] = hitchserve.Service(
            command=["python", "-u", "-m", "SimpleHTTPServer"],
            log_line_ready_checker=lambda line: "Serving" in line,
            directory=self.path.state,
        )
        
        self.services['IPython'] = hitchpython.IPythonKernelService(self.python_package)
        
        self.services['Firefox'] = hitchselenium.FirefoxService(
            firefox_binary=self.firefox_package.firefox,
            no_libfaketime=True,
            xvfb=self.settings.get("xvfb", False) or self.settings.get("quiet", False),
            
        )


        self.services.startup(interactive=False)
        
        command_executor = self.services['Firefox'].logs.json()[0]['uri']
        
        self.ipython_kernel_filename = self.services['IPython'].wait_and_get_ipykernel_filename()
        self.ipython_step_library = hitchpython.IPythonStepLibrary()
        self.ipython_step_library.startup_connection(self.ipython_kernel_filename)

        self.run_command = self.ipython_step_library.run
        self.assert_true = self.ipython_step_library.assert_true
        self.assert_exception = self.ipython_step_library.assert_exception
        self.shutdown_connection = self.ipython_step_library.shutdown_connection
        
        self.run_command("import os")
        self.run_command("""os.chdir("{}")""".format(self.path.state))
        self.run_command("from selenium import webdriver")
        self.run_command("desired_capabilities = {}")
        self.run_command(
            """driver = webdriver.Remote(command_executor="{0}", desired_capabilities=desired_capabilities)""".format(
                command_executor
            )
        )
        

        #self.cli.run(str(self.python))
        #self.cli.expect(">>>")

    def lint(self, args=None):
        """Lint the source code."""
        run(self.pip("install", "flake8"))
        run(self.python_package.cmd.flake8(*args).in_dir(self.path.project))

    def example_code(self, code):
        for line in code.split('\n'):
            self.sleep(0.5)
            self.run_command(line)

    def success_page(self):
        pass

    def sleep(self, duration):
        """Sleep for specified duration."""
        time.sleep(int(duration))

    def placeholder(self):
        """Placeholder to add a new test."""
        pass

    def pause(self, message=""):
        if hasattr(self, 'services') and self.services is not None:
            self.services.start_interactive_mode()
        self.ipython(message=message)
        if hasattr(self, 'services') and self.services is not None:
            self.services.stop_interactive_mode()

    def shell(self):
        if hasattr(self, 'services'):
            self.services.start_interactive_mode()
            import sys
            import time ; time.sleep(0.5)
            from os import path
            from subprocess import call
            if path.exists(path.join(
                path.expanduser("~"), ".ipython/profile_default/security/",
                self.ipython_kernel_filename)
            ):
                call([
                        sys.executable, "-m", "IPython", "console",
                        "--existing",
                        path.join(
                            path.expanduser("~"),
                            ".ipython/profile_default/security/",
                            self.ipython_kernel_filename
                        )
                    ])
            else:
                call([
                    sys.executable, "-m", "IPython", "console",
                    "--existing", self.ipython_kernel_filename
                ])
            self.services.stop_interactive_mode()

    def on_failure(self):
        """Stop and IPython."""
        if self.settings.get("kaching", False):
            kaching.fail()
        if self.settings.get("pause_on_failure", True):
            self.services.log(message=self.stacktrace.to_template())
            self.shell()


    def on_success(self):
        """Ka-ching!"""
        if self.settings.get("kaching", False):
            kaching.win()
        if self.settings.get("pause_on_success", False):
            self.pause(message="SUCCESS")

    def stop_services(self):
        if hasattr(self, 'services'):
            if self.services is not None:
                self.services.shutdown()

    def tear_down(self):
        """Clean out the state directory."""
        #self.shutdown_connection()
        self.stop_services()
