from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    JINS = [
            ('Erkak', 'Erkak'),
            ('Ayol', 'Ayol'),
            ('Null', 'Null'),
        ]

    STATUS_CHOICES = (
        ('Direktor', 'Direktor'),
        ('Admin', 'Admin'),
        ('Tekshiruvchi', 'Tekshiruvchi'),
        ('Bulim', 'Bulim'),
    )
    status = models.CharField(max_length=13, choices=STATUS_CHOICES)
    gender = models.CharField(max_length=6, choices = JINS)
    phone = models.CharField(max_length=13)
    photo = models.ImageField(upload_to = 'user_photos', default='default.jpg', null=True, blank=True)
    def __str__(self):
        return self.username


class Ish_turi(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ish_id = models.CharField(max_length = 5, unique=True)
    def __str__(self):
        return self.name


class Bolim(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bulim_id = models.CharField(max_length = 5, unique=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}/{self.user}'


class Xodim(models.Model):
    JINS = [
            ('Erkak', 'Erkak'),
            ('Ayol', 'Ayol'),
            ('Null', 'Null'),
        ]
    gender = models.CharField(max_length=6, choices = JINS, null = True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    photo = models.ImageField(upload_to = 'xodim_photos', default='default.jpg')
    phone = models.CharField(max_length=13, unique=True)
    ish_turi = models.ManyToManyField(Ish_turi, related_name = 'ish_turi')
    id_raqam = models.CharField(max_length = 5, unique=True)
    bulimi = models.ForeignKey(Bolim, on_delete = models.SET_NULL, null=True, related_name = 'bolim')
    def __str__(self):
        return f'{self.id_raqam}/{self.first_name}/{self.last_name}'