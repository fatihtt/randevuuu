from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceCategory, Service, Location, Currency, ServiceProvider, AvailableService, Discount, ProviderSettings, Subscriptions, Reservation, Payment, Message, Notification

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(Location)
admin.site.register(Currency)
admin.site.register(ServiceProvider)
admin.site.register(AvailableService)
admin.site.register(Discount)
admin.site.register(ProviderSettings)
admin.site.register(Subscriptions)
admin.site.register(Reservation)
admin.site.register(Payment)
admin.site.register(Message)
admin.site.register(Notification)
