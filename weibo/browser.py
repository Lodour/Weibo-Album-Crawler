from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located


class WeiboBrowser(object):

    def __init__(self):
        self._driver = webdriver.Chrome()

    def get_cookies(self):
        # 主页
        self._driver.get('http://weibo.com')
        # 二维码登陆框
        qrcode_tab = self._wait_element('//a[@node-type="qrcode_tab"]')
        qrcode_tab.click()
        # 二维码
        qrcode_img = self._wait_element('//img[@node-type="qrcode_src"]')
        # 登陆
        self._wait_element('//a[@class="gn_name"]', 300)

        cookies = {c['name']: c['value'] for c in self._driver.get_cookies()}
        return cookies

    def _wait_element(self, xpath, timeout=60):
        locator = (By.XPATH, xpath)
        condition = visibility_of_element_located(locator)
        element = WebDriverWait(self._driver, 60).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()
