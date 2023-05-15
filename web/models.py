from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.id}: {self.email}"

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}: {self.name}"

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}: {self.category.name}, {self.name}"

class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.id}: {self.name}, {self.code}"

# Accepting that, every provider with single location is independent
class ServiceProvider(models.Model):
    authorized = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, null=True, blank=True)
    service_capacity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.id}: {self.name}, {self.category.name}"
    
class Location(models.Model):
    provider = models.OneToOneField(ServiceProvider, on_delete=models.CASCADE, related_name="location")
    longitude = models.FloatField()
    latitude = models.FloatField()
    county = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    apartment = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.longitude}, {self.latitude}: {self.provider.name}"

class AvailableService(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="available_services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    available = models.BooleanField(default=False)
    time_range = models.DurationField()
    weekly_scheme = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.id}: {self.service.name}, {self.provider.name}"

class Discount(models.Model):
    name = models.CharField(max_length=100)
    available_service = models.ForeignKey(AvailableService, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    code = models.CharField(max_length=20, blank=True, null=True)
    # If false, discount will be announced and applied all orders
    only_code = models.BooleanField(default=True)
    # Discount can be both percent or amount, if both exist, percent will be taken
    percent = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

class ProviderSettings(models.Model):
    provider = models.OneToOneField(ServiceProvider, on_delete=models.CASCADE, related_name="provider_settings")
    # Example "[[09,11,13], [09,11], [], [], [], [], []]"
    #           Monday      Tuesd    W   Th   F  Sa  Su
    weekly_scheme = models.TextField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    approved_subscription = models.BooleanField(default=True)
    logo_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: Settings of {self.provider.name}"

class Subscriptions(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="subscriptions")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    approve_time = models.DateTimeField(blank=True, null=True)
    deactivate_time = models.DateTimeField(blank=True, null=True)
    customer_deactivated = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.provider.name}, {self.customer.email}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(AvailableService, on_delete=models.CASCADE, related_name="reservations")
    start_time = models.DateTimeField()
    reservation_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    deactivation_time = models.DateTimeField(blank=True, null=True)
    deactivation_reason = models.TextField(blank=True, null=True)
    realization = models.BooleanField(blank=True, null=True)
    customer_acceptance = models.DateTimeField(blank=True, null=True)
    provider_acceptance = models.DateTimeField(blank=True, null=True)
    customer_star = models.FloatField(blank=True, null=True)
    customer_note = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.user.email}, {self.service.service.name}, {self.reservation_time}"

class Payment(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="payments")
    time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    information = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.reservation.user.email}, {self.reservation.service.service.name}, on {self.time}, {self.amount} {self.currency.code}"

class Message(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    read = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: from {self.sender.email}, to {self.receiver.email}, on {self.time}"

class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    message = models.TextField()
    # e.g. "message|345" go to message_view with id=345
    code = models.TextField()

    def __str__(self):
        return f"{self.id}: {self.receiver.email}, on {self.time}, {self.title}"
    
class TempDeactivation(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="temp_deactivations")
    deactive_date = models.DateField()
    hours = models.CharField(max_length=100, blank=True, null=True)
    excuse = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.provider.name}, on {self.deactive_date}"

