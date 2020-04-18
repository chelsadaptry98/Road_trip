from django.shortcuts import render
from website.route_generation import *
# Create your views here.
def welcome(request):
    if request.method == 'GET':
        source="Bangalore"
        destination="Mysore"
        preferences=['Water','Wildlife']
        thread_create(source,destination,preferences)
        return render(request,"website/welcome.html")
    elif request.method == 'POST':
        return render(request,"website/welcome.html")