# Uncomment the required imports before adding the code


from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)
    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(data)


def logout(request):
    return JsonResponse({"userName": ""})


def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            email = data.get('email')
            first_name = data.get('firstName')
            last_name = data.get('lastName')

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': False,
                    'error': 'El usuario ya está registrado'
                })

            User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            return JsonResponse({
                'status': True,
                'userName': username
            })

        except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse(
        {'status': False, 'error': 'Método no permitido'},
        status=405
    )


@csrf_exempt
def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
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
                sentiment = analyze_review_sentiments(
                    review_detail.get('review', '')
                )
                review_detail['sentiment'] = sentiment.get(
                    'sentiment', 'unknown'
                )

            return JsonResponse({"status": 200, "reviews": reviews})

        except Exception as e:
            message = f"Error fetching reviews: {str(e)}"
            return JsonResponse({"status": 500, "message": message})

    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        try:
            dealership = get_request(endpoint)
            if dealership:
                return JsonResponse({"status": 200, "dealer": [dealership]})

            return JsonResponse({"status": 404, "message": "Dealer not found"})

        except Exception as e:
            message = f"Error fetching dealer: {str(e)}"
            return JsonResponse({"status": 500, "message": message})

    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if not request.user.is_anonymous:
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

    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]

    return JsonResponse({"CarModels": cars})
