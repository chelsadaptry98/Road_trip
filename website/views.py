from django.shortcuts import render
from website.route_generation import *
# Create your views here.

def welcome(request):
    if request.method == 'GET':
        source="Bangalore"
        destination="Mysore"
        preferences=['Water','Wildlife','Heritage']
        way=thread_create(source,destination,preferences)
        print("Way received in views",way)
        return render(request,"website/welcome.html")
    elif request.method == 'POST':
        return render(request,"website/welcome.html")