from .base_page import BasePage
from .locators import ProductPageLocators

class ProductPage(BasePage):
    def add_to_basket(self):
        button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON)
        button.click()

    def get_product_name(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text

    def get_product_price(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text

    def should_be_add_to_basket_success_message(self, expected_product_name):
        message = self.browser.find_element(*ProductPageLocators.SUCCESS_MESSAGE).text
        assert expected_product_name in message, \
            f"Expected name '{expected_product_name}' in message, got '{message}'"

    def should_be_correct_basket_total(self, expected_product_price):
        message = self.browser.find_element(*ProductPageLocators.BASKET_TOTAL_MESSAGE).text
        assert expected_product_price in message, \
            f"Expected price '{expected_product_price}' in basket total, got '{message}'"

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message is presented, but should not be"

    def should_disappear_success_message(self):
        assert self.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message didn't disappear"