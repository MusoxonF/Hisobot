from django.db import models
from User.models import *


class Photo(models.Model):
    photo = models.ImageField(upload_to='MistakeFiles/')


class Maxsulot(models.Model):
    name = models.CharField(max_length=255)
    maxsulot_id = models.CharField(max_length = 5, unique=True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    xato_id = models.CharField(max_length = 5, unique=True)
    problem_name = models.TextField()

    def __str__(self):
        return self.problem_name


class Hisobot(models.Model):
    xodim = models.ForeignKey(Xodim, on_delete=models.CASCADE, related_name='xodim')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem', null=True, blank=True)
    rasm = models.ManyToManyField(Photo, related_name='MistakesPhoto')
    files = models.FileField(upload_to = 'MistakeFiles/', null=True, blank=True)
    izoh = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE, related_name = 'maxsluot')
    xato_soni = models.PositiveIntegerField(null=True, blank=True)
    butun_soni = models.PositiveIntegerField(null=True)
    ish_vaqti = models.PositiveIntegerField(null=True)
    def __str__(self):
        return self.problem.problem_name