from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Ride)
admin.site.register(Booking)


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.safestring import mark_safe

class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'driver_status')
    
    def driver_status(self, obj):
        
        if obj.groups.filter(name="Rider").exists():
            return mark_safe('<span style="color: green;">✔️</span>')
        
        return mark_safe('<span style="color: red;">✖️</span>')  

    driver_status.short_description = 'Driver Status' 


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
