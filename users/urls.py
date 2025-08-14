from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentListAPIView,
    SubscriptionAPIView,
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserPaymentRetrieveAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    # ссылки для модели User
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("user/<int:pk>/detail/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("user/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_delete"),
    path("user/<int:pk>/payments/", UserPaymentRetrieveAPIView.as_view(), name="user_payment"),
    # ссылки для модели Payment
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
    # ссылки для регистрации/авторизации + токен
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    # ссылки для модели Subscription
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
]
