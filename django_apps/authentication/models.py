from django.db import models
from django.contrib.auth.models import User
from utils.models import BaseModelUUID


# Create your models here.
class Profile(BaseModelUUID):
    ROLE = (
            ('admin', 'admin'),
            ('sale', 'sale'),
            ('purchase', 'purchase'),
    )
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE)
    role = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=ROLE,
        default='admin'
    )

    def __str__(self):
        return self.user.email
