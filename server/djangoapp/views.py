# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provided credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout(request):
    # Terminate user session
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        try:
            # Parsear datos JSON
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            email = data.get('email')
            first_name = data.get('firstName')
            last_name = data.get('lastName')

            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': False,
                    'error': 'El usuario ya está registrado'
                })

            # Crear nuevo usuario
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            return JsonResponse({
                'status': True,
                'userName': username
            })

        except Exception as e:
            return JsonResponse({
                'status': False,
                'error': str(e)
            })

    return JsonResponse({
        'status': False,
        'error': 'Método no permitido'
    }, status=405)


@csrf_exempt
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        try:
            reviews = get_request(endpoint)
            if reviews is None:
                return JsonResponse({"status": 200, "reviews": []})

            for review_detail in reviews:
                response = analyze_review_sentiments(
                    review_detail.get('review', '')
                )
                review_detail['sentiment'] = response.get('sentiment', 'unknown')

            return JsonResponse({"status": 200, "reviews": reviews})

        except Exception as e:
            return JsonResponse({
                "status": 500,
                "message": f"Error fetching reviews: {str(e)}"
            })

    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        try:
            dealership = get_request(endpoint)
            if dealership:
                # Wrap the dealer object in an array to match Dealer.js expectation
                return JsonResponse({"status": 200, "dealer": [dealership]})
            return JsonResponse({"status": 404, "message": "Dealer not found"})

        except Exception as e:
            return JsonResponse({
                "status": 500,
                "message": f"Error fetching dealer: {str(e)}"
            })

    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if request.user.is_anonymous is False:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse({
                "status": 401,
                "message": "Error in posting review"
            })

    return JsonResponse({"status": 403, "message": "Unauthorized"})


def get_cars(request):
    count = CarModel.objects.count()
    print("Cantidad de modelos:", count)

    if count == 0:
        print("Base vacía, ejecutando populate...")
        initiate()

    car_models = CarModel.objects.select_related('car_make')

    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})
