from django.contrib import admin
from .models import UserModel, Meep, Follower

# Register your models here.
@admin.register(UserModel)
class MeepAdmin(admin.ModelAdmin):
    list_display = ['name','email','uname','password','bio','created_at','updated_at']

admin.site.register(Meep)
admin.site.register(Follower)