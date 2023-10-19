from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_staff = models.BooleanField(verbose_name="스태프 여부", default=False)
    created_at = models.DateTimeField(verbose_name="유저 정보 생성시간", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="유저 정보 수정 시간", auto_now=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        db_table = "user"