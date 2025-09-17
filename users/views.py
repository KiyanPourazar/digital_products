import random
import uuid

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import User, Device

import random
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Device


class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Missing phone number'}, status=status.HTTP_400_BAD_REQUEST)

        phone_str = str(phone_number)

        if not phone_str.isdigit() or not (11 <= len(phone_str) <= 13):
            return Response({'error': 'Phone number must be 11 to 13 digits'}, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     user = User.objects.get(phone_number=phone_number)
        #     return Response({'detail': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        # except User.DoesNotExist:
        #     user = User.objects.create_user(phone_number=phone_number)

        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                "username": f"user_{phone_number}",
                "email": f"{phone_number}@digital_product.com",
            }
        )

        if not created:
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_unusable_password()
        user.save()

        Device.objects.create(user=user)

        # OTP
        code = random.randint(100000, 999999)

        # cache
        cache.set(str(phone_number), code, 2 * 60)

        # send code (sms or email)
        return Response({'code': code}, status=status.HTTP_201_CREATED)


class GetToken(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        cached_code = cache.get(str(phone_number))

        if code != cached_code:
            return Response({'error': 'Invalid code'}, status=status.HTTP_403_FORBIDDEN)

        token = str(uuid.uuid4())

        return Response({'token': token}, status=status.HTTP_200_OK)
