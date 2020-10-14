from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="profile",
                                related_query_name='profile')
    name = models.CharField(null=False,
                            max_length=155,
                            default='')
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
