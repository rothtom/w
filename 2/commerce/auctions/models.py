from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Item(models.Model):
    title = models.CharField(max_length=48)
    description = models.CharField(max_length=128)
    picture_link = models.URLField(blank=True)
    category = models.CharField(max_length=16, blank=True)
    starting_bid = models.FloatField(max_length=12)
    def __str__(self):
        return f"{self.title} is a {self.description} in the {self.category} category"



class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    watchlisted_by = models.ManyToManyField(User, related_name="watchlist")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"The item {self.item} is listed by {self.owner} and wishlisted by {self.watchlisted_by}."


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=256)

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=12)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bidder} bidded {self.value} for {self.listing.item.title}."
