from django.db import models
from user.models import User


class Cafe(models.Model):
    name = models.CharField(max_length=24, verbose_name="카페 이름")
    user = models.ForeignKey(User, verbose_name="관리자", on_delete=models.CASCADE, null=True)
    latitude = models.DecimalField(max_digits=16, decimal_places=14, verbose_name="위도", null=True)
    longitude = models.DecimalField(max_digits=17, decimal_places=14, verbose_name="경도", null=True)
    capacity = models.IntegerField(verbose_name="수용 가능 인원", null=True)
    outlet = models.IntegerField(verbose_name="콘센트", null=True)
    floor = models.IntegerField(verbose_name="층", null=True)
    created_by = models.IntegerField(verbose_name="카페 등록 경로", default=None)
    created_at = models.DateTimeField(verbose_name="카페 정보 생성시간", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="카페 정보 수정 시간", auto_now=True)
    
    class Meta:
        db_table = "cafe"


class Comment(models.Model):
    cafe = models.ForeignKey(Cafe, verbose_name="카페 이름", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="댓글 작성자", on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="댓글 내용")
    created_at = models.DateTimeField(verbose_name="댓글 생성시간", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="댓글 수정 시간", auto_now=True)

    class Meta:
        db_table = "comment"


class Like(models.Model):
    cafe = models.ForeignKey(Cafe, verbose_name="카페 이름", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="좋아요 누른 사람", on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="좋아요 생성시간", auto_now_add=True)

    class Meta:
        db_table = "like"
