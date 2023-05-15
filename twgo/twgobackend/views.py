from decimal import Decimal, InvalidOperation
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from .serializers import CustomUserSerializer
from .models import *

from .registrations import *
from .logins import *


def index(request):
    return HttpResponse('Hello, this is my django app')


class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        money, created = Money.objects.get_or_create(user=request.user)
        balance = money.total

        return JsonResponse({'balance': balance}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        money, created = Money.objects.get_or_create(user=request.user)

        # Get the amount to add or subtract from the balance
        amount = request.data.get('amount', None)
        if amount is None:
            return JsonResponse({'error': 'Please provide an amount to change the balance'}, status=400)

        try:
            amount = Decimal(amount)
        except InvalidOperation:
            return JsonResponse({'error': 'Invalid amount provided'}, status=400)

        # Check if we are adding or subtracting from the balance
        action = request.data.get('action', None)
        if action is None:
            return JsonResponse({'error': 'Please provide an action to perform on the balance (add/sub)'}, status=400)

        if action not in ['add', 'sub']:
            return JsonResponse({'error': 'Invalid action provided. Only "add" or "sub" allowed.'}, status=400)

        # Perform the action on the balance
        if action == 'add':
            money.total += amount
        elif action == 'sub':
            if money.total < amount:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
            money.total -= amount

        # Save the changes to the balance
        money.save()

        return JsonResponse({'balance': money.total}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    sender = request.user
    subject = request.data.get('subject')
    body = request.data.get('body')
    admins = CustomUser.objects.filter(is_staff=True)
    for admin in admins:
        message = Message.objects.create(
            sender=sender, recipient=admin, subject=subject, body=body)
    return Response({'success': True})
