from django.db import IntegrityError
from django.urls import reverse

from .models import Listing, Bid, User

def get_price(listing):
    print(listing)
    try:
        price = Bid.objects.filter(listing=listing).all().order_by("-value").first().value
    except AttributeError:
        price = Listing.objects.get(pk=listing.id).item.starting_bid

    return float(price)

def get_watchlist(user_id):
    return Listing.objects.filter(watchlisted_by=User.objects.get(pk=user_id)).first()