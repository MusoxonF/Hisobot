from django.db import models
from User.models import *


class Photo(models.Model):
    photo = models.ImageField(upload_to='MistakeFiles/')


class Maxsulot(models.Model):
    name = models.CharField(max_length=255)
    mahsulot_id = models.CharField(max_length = 5, unique=True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    name = models.TextField()
    xato_id = models.CharField(max_length = 5, unique=True)

    def __str__(self):
        return self.name


class Hisobot(models.Model):
    xodim = models.ForeignKey(Xodim, on_delete=models.CASCADE, related_name='xodim')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    xato = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem', null=True, blank=True)
    photo = models.ManyToManyField(Photo, related_name='MistakesPhoto')
    audio = models.FileField(upload_to = 'MistakeFiles/', null=True, blank=True)
    izoh = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    mahsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE, related_name = 'maxsulot')
    xato_soni = models.PositiveIntegerField(default=0)
    butun_soni = models.PositiveIntegerField(default=0)
    ish_vaqti = models.PositiveIntegerField(null=True)
    def __str__(self):
        return f'{self.xodim}/{self.user}/{self.xato}/{self.mahsulot}'