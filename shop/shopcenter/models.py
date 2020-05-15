from django.db import models

# Create your models here.

class ShopUser(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    session = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.session)

class ShopItem(models.Model):
    name = models.CharField(max_length=100)
    item_cat = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    source = models.TextField()
    discription = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    was_clicked = models.BooleanField()