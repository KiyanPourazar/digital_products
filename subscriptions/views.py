
from rest_framework import status

from .models import Package, Subscription
from .serializers import PackageSerializer, SubscriptionSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subscription
from .serializers import SubscriptionSerializer

class PackageView(APIView):
    """
    لیست پکیج‌های فعال
    """
    def get(self, request):
        packages = Package.objects.filter(is_enable=True)
        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionsView(APIView):
    """
    لیست اشتراک‌های کاربر
    """
    def get(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user).select_related("package")
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        package_id = request.data.get("package_id")

        try:
            package = Package.objects.get(id=package_id, is_enable=True)
        except Package.DoesNotExist:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

        subscription = Subscription.objects.create(
            user=user,
            package=package,
        )

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
