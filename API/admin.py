from django.contrib import admin
from .models import WatchList,StreamPlatform,Review
# Register your models here.



@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ['id','title','storyline','platform','created','active']


@admin.register(StreamPlatform)

class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ['id','name','about','website']


@admin.register(Review)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id','rating','description','watchlist','created','updated','active']

