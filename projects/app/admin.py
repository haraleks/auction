from django.contrib import admin
from app.models import (UserProfile, Auction, RateMember)


admin.site.register(UserProfile)
admin.site.register(Auction)
admin.site.register(RateMember)
