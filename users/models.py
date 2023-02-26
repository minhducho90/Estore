from django.db import models
from django.contrib.auth.models import User


class KhachHang(models.Model):
    ho = models.CharField(max_length=255, blank=False)
    ten = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    mat_khau = models.CharField(max_length=50, blank=False)
    dien_thoai = models.CharField(max_length=20)
    dia_chi = models.TextField()

    def __str__(self):
        return self.ten


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    dien_thoai = models.CharField(max_length=20)
    dia_chi = models.TextField()

    def __str__(self):
        return f'{self.user.username} and {self.dien_thoai}'

    class Meta:
        db_table = u'customers'