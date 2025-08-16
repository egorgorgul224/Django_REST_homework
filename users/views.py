from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.models import Payment, Subscription, User
from users.permissions import IsModerator, IsOwnerAccount
from users.serializers import (PaymentSerializer, RegisterUserSerializer, SubscriptionSerializer,
                               UserMinInfoSerializer, UserSerializer)
from users.services import (create_stripe_price, create_stripe_product, create_stripe_session, get_cash_info,
                            get_checkout_session, transform_checkout_session_info)


class UserCreateAPIView(generics.CreateAPIView):
    """Класс generics модели User для регистрации/создания пользователя."""

    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    """Класс generics модели User для вывода списка пользователей."""

    serializer_class = UserMinInfoSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Функция для вывода необходимого сериализатора. Если пользователь 'moderator' или 'staff' - выводится вся
        информация через UserSerializer, иначе только часть информации через UserMinInfoSerializer."""

        user = self.request.user
        if user.groups.filter(name="moderator").exists() or user.is_staff:
            return UserSerializer
        return UserMinInfoSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Класс generics модели User для вывода информации о пользователе."""

    serializer_class = UserMinInfoSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Функция для вывода необходимого сериализатора. Если пользователь является владельцем или 'staff' - выводится
        вся информация через UserSerializer, иначе только часть информации через UserMinInfoSerializer."""

        user = self.request.user
        user_data = get_object_or_404(User, pk=self.kwargs["pk"])
        if user == user_data or user.is_staff:
            return UserSerializer
        return UserMinInfoSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """Класс generics модели User для обновления информации о пользователе."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwnerAccount]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Класс generics модели User для удаления пользователя."""

    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    """Класс generics модели Payment для вывода списка всех платежей по курсам и/или урокам. Реализован вывод всех
    платежей, фильтрация по полям: 'course', 'lesson' и 'method', сортировка по дате платежа."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "method")
    ordering_fields = ("created_at",)


class UserPaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Класс generics модели User для вывода информации о всех платежах пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class SubscriptionAPIView(APIView):
    """Класс APIView модели Subscription для добавления/удаления подписки пользователя на курс."""

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def post(self, request, *args, **kwargs):
        """Функция добавляет/удаляет пользователю подписку на курс. Если пользователь был подписан на курс - то
        подписка отменяется, в обратно случае подписка оформляется."""

        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.all().filter(user=user).filter(course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка отменена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка оформлена"
        return Response({"message": message})


class PaymentCreateAPIView(generics.CreateAPIView):
    """Класс generics модели Payment для создания оплаты курса."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """Метод для создания оплаты курса. Вызываются следующие функции: create_stripe_product(передается название
        курса), create_stripe_price(передается stripe product и сумма оплаты), create_stripe_session(передается stripe
        price). Результат возвращает id оплаты, сумму оплаты, id сессии, ссылку на оплату, id курса и пользователя."""

        payment = serializer.save(user=self.request.user)
        if payment.method == "transfer":
            course = create_stripe_product(payment.course.name)
            price = create_stripe_price(course, payment.course.amount)
            session_id, payment_link = create_stripe_session(price)
            payment.session_id = session_id
            payment.link = payment_link
            payment.save()
        elif payment.method == "cash":
            payment.session_id = None
            payment.link = None
            payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Класс generics модели Payment для вывода информации/статуса по оплате курса. Доступ к информации есть у админа
    или модератора."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | ~IsOwnerAccount | IsAdminUser]

    def get(self, request, *args, **kwargs):
        """Метод для получения информации о платеже."""

        user = self.request.user
        donation_object = get_object_or_404(Payment, pk=self.kwargs["pk"])
        if donation_object.method == "transfer":
            full_session_info = get_checkout_session(donation_object.session_id)
            transform_session_info = transform_checkout_session_info(user, full_session_info)
            return Response(transform_session_info)
        elif donation_object.method == "cash":
            transform_session_info = get_cash_info(user, donation_object)
            return Response(transform_session_info)
