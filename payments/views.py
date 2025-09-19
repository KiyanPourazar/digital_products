# payments/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Gateway, Payment
from .serializers import GatewaySerializer, PaymentSerializer
from subscriptions.models import Package


class GatewayView(APIView):
    """
    لیست درگاه‌های فعال
    """
    def get(self, request):
        gateways = Gateway.objects.filter(is_enable=True)
        serializer = GatewaySerializer(gateways, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentView(APIView):
    """
    ایجاد و مشاهده پرداخت‌های کاربر
    """
    def get(self, request):
        user = request.user
        payments = Payment.objects.filter(user=user).select_related("package", "gateway")
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        package_id = request.data.get("package_id")
        gateway_id = request.data.get("gateway_id")
        device_uuid = request.data.get("device_uuid")
        phone_number = request.data.get("phone_number")

        try:
            package = Package.objects.get(id=package_id, is_enable=True)
        except Package.DoesNotExist:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            gateway = Gateway.objects.get(id=gateway_id, is_enable=True)
        except Gateway.DoesNotExist:
            return Response({"error": "Gateway not found"}, status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.create(
            user=user,
            package=package,
            gateway=gateway,
            price=package.price,
            status=Payment.STATUS_VOID,
            device_uuid=device_uuid,
            phone_number=phone_number,
            consumed_code=None,
        )

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
