from django.db import models

# Create your models here.

class Test(models.Model):
    id=models.CharField(primary_key=True,max_length=30)
    sn=models.CharField(max_length=30)
    extra=models.CharField(max_length=10)
    class Meta:
        verbose_name=('test')
