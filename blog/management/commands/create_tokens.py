from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Creates auth tokens for all existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not Token.objects.filter(user=user).exists():
                Token.objects.create(user=user)
