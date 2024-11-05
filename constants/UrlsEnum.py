from enum import Enum

class UrlsEnum(Enum):


    BASE_URL = "http://localhost/opencart"
    HOME_PAGE = "/"
    CATEGORY_ENDPOINT = "/product/category"
    BROWSE_CATEGORY_ENDPOINT = "/index.php?route=product/category&path={category_id}"
    PRODUCT_ENDPOINT = "/product/product"
    VIEW_PRODUCT_ENDPOINT = "/index.php?route=product/product&product_id={product_id}"
    ADD_TO_CART_ENDPOINT = "/checkout/cart/add"
    ADD_TO_CART_FULL_ENDPOINT = "/index.php?route=checkout/cart.add"
    CHECKOUT_ENDPOINT = "/checkout"
    CHECKOUT_FULL_ENDPOINT = "/index.php?route=checkout/checkout"
    CHECKOUT_CONFIRM_ENDPOINT = "/checkout/confirm"
    CHECKOUT_CONFIRM_FULL_ENDPOINT = "/index.php?route=checkout/confirm"