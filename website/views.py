from django.shortcuts import render
from website.route_generation import *
# Create your views here.

def index(request):
	return render(request,"website/welcome.html")

def welcome(request):
    if request.method == 'GET':
        return render(request,"website/welcome.html")
    elif request.method == 'POST':
    	source = request.POST.get('source')
    	destination = request.POST.get('destination')
    	preferences = request.POST.getlist('checks[]')
    	print(source,destination,preferences)
    	way = thread_create(source,destination,preferences)
    	print("Way received in views",way)
    	s = way[0]
    	d = way[len(way) - 1]
    	w = way
    	w.remove(s)
    	w.remove(d)
    	return render(request,"website/googlemapapi.html", {'waypoints':w,'source':s,'end':d,'preferences':preferences})
    