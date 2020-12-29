import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def every_downloads_chrome(driver, i):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    a = driver.execute_script(
        'return document.querySelector("body > downloads-manager").querySelector("#frb{}").shadowRoot.querySelector("#description").textContent.search("/")'.format(
            i))
    if a == -1:
        return False
        # 这时候就睡眠

    else:
        return True

def demo():
    try:
        browser = webdriver.Chrome(executable_path='C:\MyJavaWorkspace\pydemo\driver\chromedriver.exe')
        browser.get('http://wiki.ym/login.action')
        login_name_ele = browser.find_element_by_xpath("//*[@id='os_username']")
        login_name_ele.send_keys('huangxiaocheng')
        login_pwd_ele = browser.find_element_by_xpath("//*[@id='os_password']")
        login_pwd_ele.send_keys("Yamei2019.")
        login_but_ele = browser.find_element_by_xpath("//*[@id='loginButton']")
        login_but_ele.click()

        browser.get('http://wiki.ym/pages/viewpage.action?pageId=15302789')
        extend_ele = browser.find_element_by_xpath("//*[@id='action-menu-link']")
        extend_ele.click()

        pdf_ele = browser.find_element_by_xpath("//*[@id='action-export-word-link']")
        pdf_ele.click()
        # download = every_downloads_chrome(browser, 1)
        # if not download:
        #     time.sleep(10)
        print('运行结束')
    except NoSuchElementException:
        print('seleniumn 异常')
        browser.close()



demo()