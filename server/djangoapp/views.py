import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel, Dealer, Review


def _payload(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return {}


def _sentiment(text):
    positive = {"amazing", "awesome", "excellent", "fantastic", "friendly", "good", "great", "love", "perfect", "professional"}
    negative = {"awful", "bad", "disappointing", "horrible", "poor", "rude", "terrible", "waste", "worst"}
    words = {word.strip(".,!?;:").lower() for word in text.split()}
    score = len(words & positive) - len(words & negative)
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"


def _dealer_dict(dealer):
    return {
        "id": dealer.source_id,
        "city": dealer.city,
        "state": dealer.state,
        "st": dealer.st,
        "address": dealer.address,
        "zip": dealer.zip,
        "short_name": dealer.short_name,
        "full_name": dealer.full_name,
    }


def _review_dict(review):
    return {
        "id": review.id,
        "name": review.name,
        "dealership": review.dealership.source_id,
        "review": review.review,
        "purchase": review.purchase,
        "purchase_date": review.purchase_date.isoformat() if review.purchase_date else "",
        "car_make": review.car_make,
        "car_model": review.car_model,
        "car_year": review.car_year,
        "sentiment": review.sentiment,
    }


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "POST required"}, status=405)
    data = _payload(request)
    username = data.get("userName") or data.get("username", "")
    user = authenticate(request, username=username, password=data.get("password", ""))
    if user is None:
        return JsonResponse({"userName": username, "status": "Unauthenticated"}, status=401)
    login(request, user)
    return JsonResponse({
        "userName": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "status": "Authenticated",
    })


def logout_request(request):
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({"userName": "", "message": f"Logged out {username}".strip()})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "POST required"}, status=405)
    data = _payload(request)
    username = data.get("userName") or data.get("username", "")
    password = data.get("password", "")
    if not username or not password:
        return JsonResponse({"status": 400, "message": "Username and password are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": 409, "message": "Username already exists"}, status=409)
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=data.get("firstName") or data.get("first_name", ""),
        last_name=data.get("lastName") or data.get("last_name", ""),
        email=data.get("email", ""),
    )
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated"}, status=201)


def current_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False, "userName": ""})
    return JsonResponse({
        "authenticated": True,
        "userName": request.user.username,
        "firstName": request.user.first_name,
        "lastName": request.user.last_name,
    })


def get_dealerships(request, state=None):
    dealers = Dealer.objects.all()
    if state and state.lower() != "all":
        dealers = dealers.filter(state__iexact=state)
        if not dealers.exists():
            dealers = Dealer.objects.filter(st__iexact=state)
    return JsonResponse({"status": 200, "dealers": [_dealer_dict(d) for d in dealers]})


def get_dealer_details(request, dealer_id):
    dealer = Dealer.objects.filter(source_id=dealer_id).first()
    if not dealer:
        return JsonResponse({"status": 404, "dealer": []}, status=404)
    return JsonResponse({"status": 200, "dealer": [_dealer_dict(dealer)]})


def get_dealer_reviews(request, dealer_id):
    reviews = Review.objects.filter(dealership__source_id=dealer_id)
    return JsonResponse({"status": 200, "reviews": [_review_dict(r) for r in reviews]})


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "POST required"}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"status": 401, "message": "Login required"}, status=401)
    data = _payload(request)
    dealer = Dealer.objects.filter(source_id=data.get("dealership")).first()
    if not dealer:
        return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)
    purchase_date = None
    if data.get("purchase_date"):
        try:
            purchase_date = datetime.strptime(data["purchase_date"], "%Y-%m-%d").date()
        except ValueError:
            pass
    review = Review.objects.create(
        dealership=dealer,
        name=data.get("name") or request.user.get_full_name() or request.user.username,
        review=data.get("review", ""),
        purchase=bool(data.get("purchase", True)),
        purchase_date=purchase_date,
        car_make=data.get("car_make", ""),
        car_model=data.get("car_model", ""),
        car_year=data.get("car_year") or None,
        sentiment=_sentiment(data.get("review", "")),
        created_by=request.user,
    )
    return JsonResponse({"status": 200, "review": _review_dict(review)})


def get_cars(request):
    makes = [{"id": make.id, "name": make.name, "description": make.description} for make in CarMake.objects.all()]
    models = [{
        "id": model.id,
        "CarMake": model.make.name,
        "CarModel": model.name,
        "CarType": model.type,
        "CarYear": model.year,
    } for model in CarModel.objects.select_related("make").all()]
    return JsonResponse({"status": 200, "CarMakes": makes, "CarModels": models})


@csrf_exempt
def analyze_review(request, text=None):
    if text is None:
        text = _payload(request).get("text", "")
    return JsonResponse({"text": text, "sentiment": _sentiment(text)})
