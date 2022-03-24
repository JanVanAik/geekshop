from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)




    def safe_delete(self):
        self.is_active = False
        self.save()

