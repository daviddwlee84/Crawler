# Selenium

* [SeleniumHQ/selenium: A browser automation framework and ecosystem.](https://github.com/SeleniumHQ/selenium)
* [Selenium Client Driver — Selenium 3.14 documentation](https://www.selenium.dev/selenium/docs/api/py/)

## Install WebDriver (first step)

* [WebDriver](https://w3c.github.io/webdriver/)

### ChromeDriver

#### Before ChromeDriver (Setup Chrome)

WSL

* [~~ubuntu - Running Selenium on WSL using Chrome - Super User~~](https://superuser.com/questions/1475553/running-selenium-on-wsl-using-chrome)
* [How to invoke Chromedriver from Windows Subsystem for Linux for Selenium (should work with Firefox too) from Stack Overflow: Using BashOnWindows with Selenium? #1169](http://rolandtanglao.com/2018/05/01/p1-how-to-invoke-chromedriver-from-windows-subsystem-linux/)

1. Download "chromedriver.exe" (Windows version)
2. Create file of chromedriver and set mode to executable

    ```sh
    #!/bin/sh
    chromedriver.exe "$@"
    ```

3. Ready to go

    ```py
    from selenium import webdriver
    webdriver.Chrome('./chromedriver')
    ```

#### Install ChromeDriver

* [Downloads - ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/downloads)

#### Trouble Shooting

* [python - Selenium gives "selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary" on Mac - Stack Overflow](https://stackoverflow.com/questions/46026987/selenium-gives-selenium-common-exceptions-webdriverexception-message-unknown) => Forget to install Chrome first.
  * [WebDriverError: unknown error: cannot find Chrome binary · Issue #4863 · SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium/issues/4863)

### PhantomJS

* [PhantomJS - Scriptable Headless Browser](https://phantomjs.org/)

## Tutorial

* [Python - Requests, Selenium - passing cookies while logging in - Stack Overflow](https://stackoverflow.com/questions/42087985/python-requests-selenium-passing-cookies-while-logging-in)

## Resources

* [Zenika/alpine-chrome: Chrome Headless docker images built upon alpine official image](https://github.com/Zenika/alpine-chrome)
