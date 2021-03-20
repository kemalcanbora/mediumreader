from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.wait import WebDriverWait
from settings import CROME_DRIVER, SCROLL_LIMIT
from stem.control import Controller
from selenium import webdriver
from stem import Signal
import random
import time


class MediumReader:
    def __init__(self, headless=True):
        headless_proxy = "socks5://localhost:9050"
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': headless_proxy,
            'ftpProxy': headless_proxy,
            'sslProxy': headless_proxy,
            'noProxy': ''
        })
        self.switch_ip()
        self.chrome_options = webdriver.ChromeOptions()
        if headless:
            self.chrome_options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)
        self.capabilities = dict(DesiredCapabilities.CHROME)
        proxy.add_to_capabilities(self.capabilities)

    def create_driver(self):
        return webdriver.Chrome(CROME_DRIVER,
                                desired_capabilities=self.capabilities,
                                options=self.chrome_options)

    @staticmethod
    def reader(url, driver):
        driver.get(url)
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("root"))
        for i in range(SCROLL_LIMIT):
            time.sleep(random.randrange(1, 3))
            driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
            time.sleep(1)

        return True

    @staticmethod
    def switch_ip():
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password='my password')  # password came from your torrc file
            controller.signal(Signal.NEWNYM)


def run(url):
    medium = MediumReader()
    driver = medium.create_driver()
    return medium.reader(url, driver)
