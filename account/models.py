from django.db import models
from django.conf import settings

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    frist_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)    
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.frist_name} {self.last_name} ({self.user.username})'