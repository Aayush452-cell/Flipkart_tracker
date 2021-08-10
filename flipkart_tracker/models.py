from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Link(models.Model):
    name = models.CharField(max_length=220,blank=True)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,default="")
    current_price = models.FloatField(blank=True)
    old_price = models.FloatField(default=0)
    lowest_price = models.FloatField(default=0)
    price_difference = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('price_difference','-created')