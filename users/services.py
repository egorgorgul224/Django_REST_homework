import datetime

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


def get_checkout_session(session_id):
    """Функция возвращает сведения по оплате курса пользователем."""

    session_info = stripe.checkout.Session.retrieve(
        session_id,
    )
    return session_info


def transform_checkout_session_info(user, session_data):
    """Функция преобразует json-данные по оплате курса пользователем в словарь со следующими данными: session_id,
    name, last_name, email, created_at, amount_total, payment_status. Вызывается, если метод оплаты курса не
    наличными."""

    # Преобразую дату в формате '1679600215' в дату в формате Y-m-d
    s_datetime = datetime.datetime.fromtimestamp(session_data.created)

    session = {
        "session_id": session_data.id,
        "name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "created_at": s_datetime,
        "amount_total": f"{session_data.amount_total/100} {session_data.currency}",
        "payment_status": session_data.payment_status,
    }
    return session


def get_cash_info(user, donation_object):
    """Функция создает словарь со следующими данными по оплате курса пользователем: name, last_name, email,
    course_price. Вызывается, если метод оплаты курса наличными."""

    session = {
        "name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "course_price": f"{donation_object.course.amount} rub",
    }
    return session
