from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Item(models.Model):
    title = models.CharField(max_length=48)
    description = models.CharField(max_length=128)
    picture_link = models.URLField(blank=True)
    category = models.CharField(max_length=16, blank=True)
    starting_bid = models.IntegerField(max_length=12)

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=12)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bidder} bidded {self.value} for {self.listing.title}"