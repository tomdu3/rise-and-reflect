from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

HEALTH_AREAS = [
    ("Choice 1", "Choice 1"),
    ("Choice 2", "Choice 2"),
    ("Choice 3", "Choice 3"),
    ("Choice 4", "Choice 4"),
]

class UserTimeCommitments(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',
                                related_name='commitments', on_delete=models.CASCADE)
    hours_of_sleep = models.IntegerField(blank=True, null=True)
    work_time_from = models.TimeField(blank=True, null=True)
    work_time_to = models.TimeField(blank=True, null=True)
    commute_time = models.IntegerField(blank=True, null=True)
    get_ready_time = models.IntegerField(blank=True, null=True, default=0)
    wake_time = models.TimeField(blank=True, null=True)
    
class UserHealthArea(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',
                                related_name='health_area', on_delete=models.CASCADE)
    health_area = models.CharField(max_length=9, choices=HEALTH_AREAS)