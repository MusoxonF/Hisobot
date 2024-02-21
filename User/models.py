from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    JINS = [
            ('male', 'Male'),
            ('female', 'Female'),
        ]

    STATUS_CHOICES = (
        ('admin', 'Admin'),
        ('tekshiruvchi', 'Tekshiruvchi'),
        ('bolim', 'Bolim'),
    )
    status = models.CharField(max_length=13, choices=STATUS_CHOICES)
    gender = models.CharField(max_length=6, choices = JINS)
    phone = models.CharField(max_length=13)
    image = models.ImageField(upload_to = 'user_photos', default='default.jpg')
    def __str__(self):
        return self.username


class Ish_turi(models.Model):
    ish_name = models.CharField(max_length=100)
    ish_id = models.CharField(max_length = 5, unique=True)
    def __str__(self):
        return self.ish_name


class Bolim(models.Model):
    name = models.CharField(max_length=100)
    bolim_id = models.CharField(max_length = 5, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Xodim(models.Model):
    JINS = [
            ('male', 'Male'),
            ('female', 'Female'),
        ]
    gender = models.CharField(max_length=6, choices = JINS, null = True)
    name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    image = models.ImageField(upload_to = 'xodim_photos', default='default.jpg')
    phone = models.CharField(max_length=13, unique=True)
    ish_turi = models.ManyToManyField(Ish_turi, related_name = 'ish_turi')
    xodim_id = models.CharField(max_length = 5, unique=True)
    bolimi = models.ForeignKey(Bolim, on_delete = models.CASCADE, related_name = 'bolim')
    def __str__(self):
        return self.name