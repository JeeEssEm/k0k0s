from django.db import models
from django.conf import settings
from django.db.models import ImageField, CharField, TextField
from django.urls import reverse

class Product(models.Model):
    MOODS = [
        ('MELANCHOLIC' , 'Melancholic'),
        ('WILD','Wild'),
        ('FUNNY', 'Funny'),
        ('MORALLY_GRAY', 'Morally Gray')
    ]
    title = models.CharField(max_length=200, default = "")
    price = models.IntegerField(default=0)
    mood = models.CharField(
        max_length= 50,
        choices=MOODS,
        default = 'MORALLY_GRAY'
    )
    #meme = ImageField()
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        default=''
    )

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'main:product_detail',
            args=[self.id]
        )

class User(models.Model):
    nickname=models.CharField(max_length=50)

class LikedProduct(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=''
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Order(models.Model):

    STATUSES = [
        ('PAID', 'Paid'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered')
    ]

    products = models.ManyToManyField(Product)
    status = models.CharField(
        max_length=50,
        choices=STATUSES,
        default = 'PAID'
    )
    price = models.IntegerField(default=0)


    def __str__(self):
        return self

