from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display=["username","password"]

@admin.register(Game)
class GamesAdmin(admin.ModelAdmin):
    list_display=["username","group_name","cards_list","game_starting_player","start_distribution"]
    
    def get_username(self, obj):
        return obj.username.username

@admin.register(CardContainer)
class CardContainerAdmin(admin.ModelAdmin):
    list_display=['group_name','username','card_done','playing_card']