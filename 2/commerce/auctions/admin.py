from django.contrib import admin
from .models import Bid, Item, Listing, User, Comment
# Register your models here.


admin.site.register(Bid)
admin.site.register(Item)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Comment)
