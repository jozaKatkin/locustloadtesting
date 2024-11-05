import random
import threading
from functools import wraps

from locust import HttpUser, task, between
from prometheus_client import Counter, start_http_server, Histogram

from constants.UrlsEnum import UrlsEnum
from constants.HTTPMethod import HTTPMethod

REQUEST_TIME = Histogram('locust_request_duration_seconds', 'Request latency', ['endpoint', 'method'])
REQUESTS = Counter('locust_requests_total', 'Total number of requests', ['endpoint', 'method', 'status'])


def start_metrics_server():
    try:
        print("Starting Prometheus metrics server on port 8000...")
        start_http_server(8000)
        print("Prometheus metrics server started on port 8000")
    except Exception as e:
        print(f"Error starting metrics server: {e}")


thread = threading.Thread(target=start_metrics_server)
thread.daemon = True
thread.start()

def track_metrics(endpoint, method):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with REQUEST_TIME.labels(endpoint=endpoint, method=method).time():
                response = func(self, *args, **kwargs)
            status_code = getattr(response, 'status_code', 'N/A')
            REQUESTS.labels(endpoint=endpoint, method=method, status=str(status_code)).inc()
            return response
        return wrapper
    return decorator

class UserBehaviour(HttpUser):
    wait_time = between(1, 5)
    host = UrlsEnum.BASE_URL.value
    products = [28, 29, 40, 51, 52, 54, 55, 56, 57, 58]

    @task
    @track_metrics(endpoint=UrlsEnum.HOME_PAGE.value, method=HTTPMethod.GET.value)
    def load_homepage(self):
        return self.client.get(UrlsEnum.HOME_PAGE.value)

    @task(2)
    @track_metrics(endpoint=UrlsEnum.CATEGORY_ENDPOINT.value, method=HTTPMethod.GET.value)
    def browse_category(self):
        category_id = 24
        return self.client.get(UrlsEnum.BROWSE_CATEGORY_ENDPOINT.value.format(category_id=category_id))

    @task(3)
    @track_metrics(endpoint=UrlsEnum.PRODUCT_ENDPOINT.value, method=HTTPMethod.GET.value)
    def view_product(self):
        product_id = random.choice(self.products)
        return self.client.get(UrlsEnum.VIEW_PRODUCT_ENDPOINT.value.format(product_id=product_id))

    @task(1)
    @track_metrics(endpoint=UrlsEnum.ADD_TO_CART_ENDPOINT.value, method=HTTPMethod.POST.value)
    def add_to_cart(self):
        product_id = random.choice(self.products)
        return self.client.post(UrlsEnum.ADD_TO_CART_FULL_ENDPOINT.value, data={
            "product_id": product_id,
            "quantity": 1
        })

    @task(1)
    @track_metrics(endpoint=UrlsEnum.CHECKOUT_ENDPOINT.value, method=HTTPMethod.GET.value)
    def checkout_get(self):
        return self.client.get(UrlsEnum.CHECKOUT_FULL_ENDPOINT.value)

    @task(1)
    @track_metrics(endpoint=UrlsEnum.CHECKOUT_CONFIRM_ENDPOINT.value, method=HTTPMethod.POST.value)
    def checkout_post(self):
        return self.client.post(UrlsEnum.CHECKOUT_CONFIRM_FULL_ENDPOINT.value)
