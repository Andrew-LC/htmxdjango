from django.db import models

# Create your models here.
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.first
