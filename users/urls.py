from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserPaymentRetrieveAPIView, UserUpdateAPIView

app_name = UsersConfig.name


urlpatterns = [
    # ссылки для модели User
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("user/<int:pk>/payments/", UserPaymentRetrieveAPIView.as_view(), name="user_payment"),
    # ссылки для модели Payment
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
]
