import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product_name):
    """Функция создает продукт в stripe."""

    return stripe.Product.create(name=product_name)


def create_stripe_price(product, amount):
    """Функция создает цену в stripe и возвращает цену в российских рублях."""

    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount) * 100,
        product_data={"name": product.get("name")},
    )


def create_stripe_session(price):
    """Функция создает сессию и возвращает id сессии и ссылку на оплату."""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
