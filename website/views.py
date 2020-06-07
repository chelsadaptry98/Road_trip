from django.shortcuts import render
from website.route_generation import *
from website.Weather_prediction import *
# Create your views here.

def index(request):
	return render(request,"website/welcome.html")

def createmap(request):
	if request.method == 'GET':
		return render(request,"website/welcome.html")

	elif request.method == 'POST':
		source=request.POST['source']
		destination=request.POST['destination']
		preferences=request.POST.getlist('preferences []')
		print("Source",source,"Destination",destination,"Preferences",preferences)
		way=thread_create(source,destination,preferences)
		print(request.POST)
		print("Way received in views",way)
		s = way[0]
		d = way[len(way) - 1]
		w = way
		w.remove(s)
		w.remove(d)
		months=weather_prediction(w)
		return render(request,"website/googlemapapi.html", {'waypoints':w,'source':s,'end':d,'preferences':preferences,'months':months})
    
def search(request):
	return render(request,"website/search.html")
