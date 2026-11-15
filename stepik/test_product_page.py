import pytest
import time
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.basket_page import BasketPage

LINK = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"

class TestUserAddToBasketFromProductPage():
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        # Регистрация пользователя перед каждым тестом
        login_link = "http://selenium1py.pythonanywhere.com/en-gb/accounts/login/"
        page = LoginPage(browser, login_link)
        page.open()
        email = str(time.time()) + "@fakemail.org"
        password = "TestPassword123!"
        page.register_new_user(email, password)
        page.should_be_authorized_user()

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        page = ProductPage(browser, LINK)
        page.open()
        expected_name = page.get_product_name()
        expected_price = page.get_product_price()
        page.add_to_basket()
        page.should_be_add_to_basket_success_message(expected_name)
        page.should_be_correct_basket_total(expected_price)

    def test_user_cant_see_success_message(self, browser):
        page = ProductPage(browser, LINK)
        page.open()
        page.should_not_be_success_message()


@pytest.mark.need_review
def test_guest_can_add_product_to_basket(browser):
    # Если нужен промокод, используйте ссылку с ?promo=newYear2019
    link_with_promo = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"
    page = ProductPage(browser, link_with_promo)
    page.open()
    expected_name = page.get_product_name()
    expected_price = page.get_product_price()
    page.add_to_basket()
    page.solve_quiz_and_get_code() # Вызов капчи
    page.should_be_add_to_basket_success_message(expected_name)
    page.should_be_correct_basket_total(expected_price)

@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.go_to_basket_page()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()

@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.go_to_login_page()
    login_page = LoginPage(browser, browser.current_url)
    login_page.should_be_login_page()

# Негативные тесты (дополнительные из предыдущего задания)
def test_guest_cant_see_success_message(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.should_not_be_success_message()

def test_message_disappeared_after_adding_product_to_basket(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.add_to_basket()
    page.should_disappear_success_message()