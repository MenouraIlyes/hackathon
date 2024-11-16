from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from hackathon.settings import mongo_db

@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        users_collection = mongo_db.get_collection("users")
        result = users_collection.insert_one(data)
        return JsonResponse({"id": str(result.inserted_id)}, status=201)

@csrf_exempt
def get_users(request):
    if request.method == "GET":
        users_collection = mongo_db.get_collection("users")
        users = list(users_collection.find({}, {"_id": 0}))
        return JsonResponse({"users": users}, status=200)
