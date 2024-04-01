import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def create_post(request):
    if request.method != "POST":
        # returns error_message if request-method is not POST;
        return JsonResponse([{
            "message": "must be accessed via GET request!"
            }], safe=False)
    
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")
        author = request.user
        post = Post.objects.create(message=message, author=author)
        return JsonResponse([{
            "message": "Post posted!"
        }], safe=False)
    
    if request.method == "PUT":
        #gets the post
        post_id = request.POST["post_id"]
        post = Post.objects.get(pk=post_id)

        #gets the new message
        message = request.POST["message"]
        #overwrites the old message
        post["message"] = message
        #saves the post
        post.save()
        return JsonResponse([{
            "message": "Post changed succesfully!"
        }])

@csrf_exempt
def get_posts(request, category, page_number):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
    if category == "all":
        posts = Post.objects.order_by("-timestamp").all()

    elif category == "following":
        if not request.user.is_authenticated:
            return JsonResponse({ "message": "must be logged in" })
        following = user.following
        posts = []

        for person in following:
            persons_posts = Post.objects.filter(author=person)
            posts.append(persons_posts)

    else: 
        return JsonResponse([{"message": "invalid category"}])



    post_list = []
    for post in posts:
        if request.user.is_authenticated:
            if post in user.liked.all():
                liked = True
            else:
                liked = False
        else:
            liked = None
        post = post.serialize()
        post["liked"] = liked
        post_list.append(post)
    p = Paginator(post_list, 10)
    try:
        page = p.page(page_number)
    except EmptyPage:
        return JsonResponse([{"message": "Invalid page number"}])


    page_content = {"body": page.object_list,
                    "message": "Succesfully selected posts",
                    "context": {
                        "has_next": page.has_next(),
                        "has_previous": page.has_previous(),
                        "page_number": page_number,
                        "page_count": p.num_pages,
                        "category": category
                    }}
    return JsonResponse(page_content, safe=False)


def display_posts(request, category, page_number):
    return index(request)


@csrf_exempt
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "user doesnt exist"})
    if username == request.user.username:
        me = True
    else:
        me = False

    posts = Post.objects.filter(author=user)

    user_data = {
        "username": user.username,
        "following": len(user.following.all()),
        "followers": len(User.objects.filter(following=user).all()),
        "self": me,
        "posts": posts
    }
    data = {"body": user_data,
            "message": "Successfully selected User",
            "logged_in": request.user.is_authenticated
            }
    print(data)
    return render(request, "network/profile.html", data)
