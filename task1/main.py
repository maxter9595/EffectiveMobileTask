import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException


def get_driver():
    """Инициализирует драйвер браузера и возвращает его"""
    browsers = {
        'Chrome': webdriver.Chrome,
        'Firefox': webdriver.Firefox,
        'Edge': webdriver.Edge,
        'Safari': webdriver.Safari,
    }
    for name, browser in browsers.items():
        try:
            driver = browser()
            print(f"Используется браузер: {name}")
            return driver
        except WebDriverException:
            print(f"{name} не установлен или драйвер недоступен.")
    raise Exception("Нет доступных браузеров.")


def wait_for_element(driver, by, value, timeout=3):
    """Ожидает появления элемента на странице"""
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    time.sleep(timeout)
    return element


def login(driver, username, password):
    """Выполняет вход в систему"""
    wait_for_element(driver, By.ID, 'user-name').send_keys(username)
    wait_for_element(driver, By.ID, 'password').send_keys(password)
    wait_for_element(driver, By.XPATH, '//*[@id="login-button"]').click()


def add_to_cart(driver):
    """Добавляет товар в корзину"""
    wait_for_element(driver, By.ID, 'add-to-cart-sauce-labs-backpack').click()


def proceed_to_checkout(driver):
    """Переходит к оформлению заказа"""
    wait_for_element(driver, By.CLASS_NAME, 'shopping_cart_link').click()
    wait_for_element(driver, By.XPATH, '//button[@data-test="checkout"]').click()


def fill_checkout_info(driver, first_name, last_name, zip_code):
    """Заполняет информацию для оформления заказа"""
    wait_for_element(driver, By.ID, 'first-name').send_keys(first_name)
    wait_for_element(driver, By.ID, 'last-name').send_keys(last_name)
    wait_for_element(driver, By.ID, 'postal-code').send_keys(zip_code)
    wait_for_element(driver, By.XPATH, '//input[@data-test="continue"]').click()


def finish_checkout(driver):
    """Завершает оформление заказа"""
    wait_for_element(driver, By.XPATH, '//button[@data-test="finish"]').click()


def check_success(driver):
    """Проверяет, завершена ли покупка успешно"""
    try:
        success_message = wait_for_element(driver, By.CLASS_NAME, 'complete-header')
        return True
    except NoSuchElementException:
        return False


def return_home(driver):
    """Возвращается на главную страницу продуктов"""
    wait_for_element(driver, By.ID, "back-to-products").click()


class TestSauceDemo(unittest.TestCase):
    def setUp(self):
        """Создает драйвер перед каждым тестом"""
        self.driver = get_driver()
        self.driver.get('https://www.saucedemo.com/')

    def tearDown(self):
        """Закрывает драйвер после каждого теста"""
        self.driver.quit()

    def test_purchase_process(self):
        """Проверяет успешное завершение покупки"""
        login(self.driver, 'standard_user', 'secret_sauce')
        add_to_cart(self.driver)
        proceed_to_checkout(self.driver)
        fill_checkout_info(self.driver, 'John', 'Doe', '12345')
        finish_checkout(self.driver)

        success_message = check_success(self.driver)
        return_home(self.driver)

        self.assertIs(success_message, True)


if __name__ == '__main__':
    unittest.main()
