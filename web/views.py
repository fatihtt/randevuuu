from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q
import json

from .models import User, Reservation, Subscriptions, ServiceProvider, AvailableService

# Create your views here.
def index(request):
    my_reservations = None
    my_subscriptions = None

    if request.user.is_authenticated:
        my_reservations = Reservation.objects.filter(user=request.user)

        my_subscriptions = Subscriptions.objects.filter(customer=request.user)
    else:
        return HttpResponseRedirect("login")
    
    return render(request, "web/index.html", {
        "my_reservations": my_reservations,
        "my_subscriptions": my_subscriptions
    })

def view_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("./")

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["input-login-email"]
        password = request.POST["input-login-pass"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "web/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "web/login.html")
    
def view_signup(request):
    try:
        message = None
        email = None
        if request.method == "POST":
            # username will be set to email
            email = request.POST["input-sign-up-email"]
            username = email

            # Ensure password matches confirmation
            password = request.POST["input-sign-up-pass"]
            confirmation = request.POST["input-sign-up-pass-confirm"]
            if password != confirmation:
                raise Exception("Passwords must match.")
            
            if len(password) < 4:
                raise Exception("Password must be at least 4 charachters")

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "web/sign-up.html", {
                    "message": "Email already in use.",
                    "email": email
                })
            
            login(request, user)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "web/sign-up.html")
    except Exception as e:
        return render(request, "web/sign-up.html", {
                    "message": e,
                    "email": email
        })

    
def view_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def view_search(request):
    try:
        if request.method != "POST":
            raise Exception("Wrong method")
        
        # Take search text
        search_text = json.loads(request.body.decode('utf-8'))["text"]

        # Search in Provider name, city, district
        providers = ServiceProvider.objects.filter(Q(name__contains=search_text) | Q(location__city__contains=search_text) | Q(location__district__contains=search_text))
        print("search result: ", providers)
        providers_cooked = []
        # Cook providers
        for provider in providers:
            # Cook available services
            available_services = AvailableService.objects.filter(provider=provider, available=True)
            available_services_cooked = []
            for available_service in available_services:
                available_service_cooked = {
                    "id": available_service.id,
                    "name": available_service.service.name
                }
                available_services_cooked.append(available_service_cooked)
            
            # Cook provider
            provider_cooked = {
                "id": provider.id,
                "name": provider.name,
                "logo_url": provider.provider_settings.logo_url,
                "city": provider.location.city,
                "district": provider.location.district,
                "available_services": available_services_cooked
            }
            providers_cooked.append(provider_cooked)
        return JsonResponse({"data": providers_cooked}, status=201)
    except Exception as e:
        print("error: ", e)
        return JsonResponse({"message": e}, status=500)