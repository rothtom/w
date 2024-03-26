from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Bid, Item, Comment
from . import util
from . import forms
from .forms import BidForm, CommentForm


def index(request):
    listings = Listing.objects.all()
    price_dict = {}
    for listing in listings:
        price = util.get_price(listing)
        price_dict[listing] = f"{price:.2f}"
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "price_dict": price_dict
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html")
    
    title = request.POST["title"]
    description = request.POST["description"]
    picture_link = request.POST["picture_link"]
    category = request.POST["category"]
    starting_bid = request.POST["starting_bid"]
    try:
        starting_bid = float(starting_bid)
    except:
        return HttpResponseRedirect(reverse("create_listing"))
    starting_bid = f"{starting_bid:.2f}"
    user_id = request.user.id

    user = User.objects.get(pk=user_id)

    item = Item.objects.create(title=title, description=description, picture_link=picture_link, category=category, starting_bid=starting_bid)
    Listing.objects.create(owner=user, item=item)

    return HttpResponseRedirect(reverse("index"))

def listing(request, listing_id):
    if watchlisted := User.objects.filter(watchlist=listing_id):
        watchlisted = True
    else:
        watchlisted = False
    try:
        listing = Listing.objects.get(pk=listing_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    price = util.get_price(listing)
    price = f"{price:.2f}"
    winner = None
    if listing.active == False:
        winner = Bid.objects.filter(listing=listing_id).all().order_by("-value").first().bidder

    comments = Comment.objects.filter(listing=listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlisted": watchlisted,
        "price": price,
        "BidForm": BidForm(),
        "winner": winner,
        "comments": comments,
        "CommentForm": CommentForm(),
    })

def remove_from_watchlist(request):
    user = User.objects.get(pk=request.user.id)
    listing_id = request.POST["remove_from_watchlist_listing_id"]
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlisted_by.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id)))


def add_to_watchlist(request):
    user = request.user
    listing_id = request.POST["add_to_watchlist_listing_id"]

    listing = Listing.objects.get(pk=listing_id)
    listing.watchlisted_by.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id)))


def delete_listing(request):
    listing_id = request.POST["delete_listing_id"]
    try:
        listing = Listing.objects.get(pk=listing_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    if listing.owner.id != request.user.id:
        return HttpResponseRedirect(reverse("listing", args=(listing_id)))
    listing.delete()
    return HttpResponseRedirect(reverse("index"))


def bid(request):
    listing_id = request.POST.get("bid_listing_id", 1)
    if request.method != "POST":
        return HttpResponseRedirect(reverse("listing", args=(listing_id)))

    bid = BidForm(request.POST)
    if not bid.is_valid():
        return HttpResponseRedirect(reverse("listing", args=(listing_id)))
    listing = Listing.objects.get(pk=listing_id)
    if listing.active == False:
        return HttpResponseRedirect(reverse("listing", args=(listing_id)))
    highest_bid = util.get_price(listing)
    user = User.objects.get(pk=request.user.id)
    bid_value = bid.cleaned_data["value"]
    if highest_bid == None:
        starting_bid = int(Listing.objects.get(pk=listing_id).item.starting_bid)
        if bid_value >= starting_bid:
            Bid.objects.create(bidder=user, value=bid_value, listing=listing)

    else:
        if bid_value > highest_bid:
            Bid.objects.create(bidder=user, value=bid_value, listing=listing)

    return HttpResponseRedirect(reverse("listing", args=(listing_id)))
                

def close_auction(request):
    listing_id = request.POST["close_listing_id"]
    listing = Listing.objects.get(pk=listing_id)
    if request.user.id == listing.owner.id:
        listing.active = False
        listing.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id)))


def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    user = User.objects.get(pk=request.user.id)
    watchlist = user.watchlist.all()
    

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist 
    })


def comment(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    
    listing_id = request.POST["listing_id"]
    listing = Listing.objects.get(pk=listing_id)
    message = request.POST["message"]
    if message == None:
        return HttpResponseRedirect(reverse("index"))

    comment = Comment.objects.create(listing=listing, author=request.user, message=message)
    return HttpResponseRedirect(reverse("listing", args=(listing_id)))

def list_categories(request):
    listings = Listing.objects.all()
    categories = []
    for listing in listings:
        if listing.item.category not in categories and listing.item.category != "":
            categories.append(listing.item.category)
    return render(request, "auctions/list_categories.html", {
        "categories": categories
    })

def display_category(request, category):
    items = Item.objects.filter(category=category)
    listings = []
    price_dict = {}
    for item in items:
        listing = Listing.objects.get(item=item)
        if listing:
            listings.append(listing)
            price_dict[listing] = f"{util.get_price(listing):.2f}"
    print(listings)
    return render(request, "auctions/display_category.html", {
        "listings": listings,
        "category": category,
        "price_dict": price_dict
    })

#completed