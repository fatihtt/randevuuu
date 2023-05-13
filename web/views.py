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
from datetime import datetime

from .models import User, Reservation, Subscriptions, ServiceProvider, AvailableService, Payment

# Create your views here.
def index(request):
    my_reservations = None
    my_subscriptions = None

    if request.user.is_authenticated:
        my_reservations = Reservation.objects.filter(user=request.user, active=True, start_time__gt=datetime.now())

        my_subscriptions = Subscriptions.objects.filter(customer=request.user, deactivate_time=None)
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
        search_term = json.loads(request.body.decode('utf-8'))["text"]

        search_term = search_term.upper()
        # Search in Provider name, city, district
        providers = ServiceProvider.objects.filter(Q(name__icontains=search_term) | Q(location__city__icontains=search_term) | Q(location__district__icontains=search_term))
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
    
def view_reservation(request, reservation_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("login")
    
    try:
        try:
            reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        except:
            raise Exception("No reservation found!")

        # Adjust remaining text
        remaining = reservation.start_time.replace(tzinfo=None) - datetime.now()
        remaining_text = f"{remaining.days} days, {remaining.seconds//3600} hours and {(remaining.seconds//60)%60} minutes"

        if reservation.start_time.replace(tzinfo=None) < datetime.now():
            remaining_text = "Passed"

        # Adjust location info
        locat = reservation.service.provider.location
        location_text = f"{locat.district}, {locat.city}"

        # Adjust payment info
        payment_done = False
        payments = reservation.payments
        print("payment count: ", payments.count())
        if payments.count() > 0:
            payment_done = True
        reservation_cooked = {
            "id": reservation.id,
            "service_name": reservation.service.service.name,
            "provider_id": reservation.service.provider.id,
            "provider_name": reservation.service.provider.name,
            "service_time": reservation.start_time,
            "remaining": remaining_text,
            "remaining_days": remaining.days,
            "location": location_text,
            "longitude": locat.longitude,
            "latitude": locat.latitude,
            "payment_done": payment_done,
            "active": reservation.active
        }
        return render(request, "web/reservation.html", {
            "res": reservation_cooked
        })
    except Exception as e:
        return render(request, "web/reservation.html", {
            "message": e
        })

def view_provider(request, provider_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("login")
    
    try:
        try:
            provider = ServiceProvider.objects.get(id=provider_id)
        except:
            raise Exception("No provider found!")
        
        # Adjust location info
        locat = provider.location
        location_text = f"{locat.district}, {locat.city}"

        # Adjust total reservations, realized reservations, rating
        available_services = provider.available_services
        reserv_count = 0
        realized_reservations = 0

        # Rating elements
        total_stars = 0
        star_count = 0

        # "Your history" elements
        your_reserv_count = 0
        your_reserv_realized_count = 0
        your_unrated_reservations = []
        
        for available_service in available_services.all():
            reserv_count = reserv_count + available_service.reservations.count()
            realized_reservations = realized_reservations + available_service.reservations.filter(realization=True).count()
            for reservation in available_service.reservations.all():
                if reservation.user == request.user:
                    your_reserv_count = your_reserv_count + 1
                    if reservation.realization:
                        your_reserv_realized_count = your_reserv_realized_count + 1
                        if not reservation.customer_star:
                            your_unrated_reservations.append(reservation)
                # for rating 
                if reservation.realization and reservation.customer_star:
                    total_stars = total_stars + reservation.customer_star
                    star_count = star_count + 1
        
        if star_count > 10:
            star_avg = total_stars / star_count
        else:
            star_avg = -1

        active_reservations = Reservation.objects.filter(user=request.user, service__provider=provider, active=True, start_time__gt=datetime.now()).exclude(realization=True)

        # Adjust active reservation
        if active_reservations.count() > 1:
            raise Exception("You have more than one active reservation")
        
        active_reservation = None
        
        if active_reservations.count() == 1:
            active_reservation = active_reservations[0]
            
        # Adjust subscription information
        y_subscriptions = request.user.subscriptions.filter(provider=provider, deactivate_time=None)
        you_subscribed = y_subscriptions.count() == 1
        subscription_approved = False
        if you_subscribed:
            subscription_approved = y_subscriptions[0].approve_time != None



        provider_cooked = {
                "id": provider.id,
                "name": provider.name,
                "logo_url": provider.provider_settings.logo_url,
                "location": location_text,
                "longitude": locat.longitude,
                "latitude": locat.latitude,
                "phone": provider.phone,
                "total_reservations": reserv_count,
                "realized_reservations": realized_reservations,
                "subscribers": provider.subscriptions.count(),
                "star_avg": star_avg,
                "your_reserv_count": your_reserv_count,
                "your_reserv_realized_count": your_reserv_realized_count,
                "your_unrated_reservations": your_unrated_reservations,
                "active_reservation": active_reservation,
                "you_subscribed": you_subscribed,
                "subscription_approved": subscription_approved
            }
        return render(request, "web/provider.html", {
            "provider": provider_cooked
        })
    except Exception as e:
        print("error", e)
        return render(request, "web/provider.html", {
            "message": e
        })

def view_new_reservation(request, provider_id):

    provider = {"name": "Service Provider"}

    active_services = [{"id": 1, "name": "Headcut"}, {"id": 2, "name": "Beardcut"}]

    return render(request, "web/new-reservation.html", {
        "provider": provider,
        "active_services": active_services
    })
    
def view_subscribe(request):
    try:
        if not request.user.is_authenticated:
            raise Exception("Authorization needed!")
        
        # Check method
        if request.method != "POST":
            raise Exception("Wrong method!")
        
        # Check providerId
        provider_id = json.loads(request.body.decode('utf-8'))["provider_id"]

        print("tip:", type(provider_id))
        if not provider_id or not type(provider_id) == type(1):
            raise Exception("Wrong provider!")
        
        # Take provider
        m_provider = None
        try:
            m_provider = ServiceProvider.objects.get(id=provider_id)
        except:
            raise Exception("Wrong provider !!")
        
        # Check prior subscription
        has_prior_subscription = False
        prior_subscription = None
        if m_provider.subscriptions.filter(customer=request.user).count() > 0:
            deactive_subscriptions = m_provider.subscriptions.filter(customer=request.user).exclude(deactivate_time=None)
            if deactive_subscriptions.count() == 1:
                # Activate deactive subscription
                has_prior_subscription = True
                prior_subscription = deactive_subscriptions[0]
            else:
                raise Exception("Already subscribed!")

        m_approve_time = None
        if not m_provider.provider_settings.approved_subscription:
            m_approve_time = datetime.now()
        

        # Create new subscription or update old deactivated subscription
        if not has_prior_subscription:
            new_subs = Subscriptions(provider=m_provider, customer=request.user, approve_time=m_approve_time)
            new_subs.save()
        else:
            prior_subscription.deactivate_time = None
            prior_subscription.customer_deactivated = None
            if not m_provider.provider_settings.approved_subscription:
                prior_subscription.approve_time = datetime.now()
            else:
                prior_subscription.approve_time = None
            prior_subscription.save()

        # raise Exception("ne demek")
        return JsonResponse({"data":"Hello from json response"}, status=201)
    except Exception as e:
        return JsonResponse({"message": str(e) }, status=401)
    
def unsubscribe(request):
    try:
        # Check authentication
        if not request.user.is_authenticated:
            raise Exception("Unauthorized request.")
        
        # Check request method
        if request.method != "POST":
            raise Exception("Wrong method.")
        
        # Take provider_id
        provider_id = json.loads(request.body.decode('utf-8'))["provider_id"]

        if not provider_id:
            raise Exception("No provider info.")
        
        provider_id = int(provider_id)

        # Check-Take ServiceProvider
        m_provider = None

        try:
            m_provider = ServiceProvider.objects.get(id=provider_id)
        except:
            raise Exception("No provider.")
        
        # Check-Take Subscription
        m_subscription = None
        try:
            m_subscription = Subscriptions.objects.get(provider=m_provider, customer=request.user, deactivate_time=None)
        except:
            raise Exception("No proper subscription")
        
        # Check-Take Active Reservations
        try:
            active_reservations = Reservation.objects.filter(user=request.user, service__provider=m_provider, active=True, start_time__gt=datetime.now())
        except:
            raise Exception("Fault while taking active reservations")
        
        # Make changes for unsubscription
        m_subscription.deactivate_time = datetime.now()
        m_subscription.customer_deactivated = True
        m_subscription.save()

        # Deactivate active reservations
        for active_reservation in active_reservations:
            active_reservation.active = False
            active_reservation.deactivation_time = datetime.now()
            active_reservation.deactivation_reason = "Unsubscription"
            active_reservation.save()

        return JsonResponse({"result": 0, "message": "subscription deactivated"}, status=201)

    except Exception as e:
        print("unsbuscription error: ", str(e))
        return JsonResponse({"result": 1, "message": str(e)}, status=401)
    
def cancel_reservation(request):
    try:
        # Check authentication
        if not request.user.is_authenticated:
            raise Exception("Unauthorized request.")
        
        # Check request method
        if request.method != "POST":
            raise Exception("Wrong method.")
        
        # Take reservation_id
        reservation_id = json.loads(request.body.decode('utf-8'))["reservation_id"]
        
        # Check - Take reservation
        if not reservation_id:
            raise Exception("No reservation number.")
        
        m_reservation = None
        try:
            m_reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        except:
            raise Exception("No reservation.")
        
        # Check reservation last 24h
        remaining = m_reservation.start_time.replace(tzinfo=None) - datetime.now()

        if remaining.days > 0:
            m_reservation.active = False
            m_reservation.deactivation_time = datetime.now()
            m_reservation.save()
            
            return JsonResponse({"succeed": 0, "message": "reservation canceled"}, status=201)
        else:
            raise Exception("No time for cancelation.")
        

    except Exception as e:
        return JsonResponse({"succeed": 1, "error": str(e)}, status=401)