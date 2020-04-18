import itertools
import pandas as pd
import googlemaps
from website.models import Waypoints,Distance
import threading
import time

bucket_size=500
last=[]

def getwaypoints(source,destination,preferences):
    waypoints=[]
    for preference in preferences:
        waypoint=[]
        wp=Waypoints.objects.filter(category__iexact=preference).exclude(district__iexact=source).exclude(district__iexact=destination)
        for w in wp:
            waypoint.append(w.name)
        waypoints.append(waypoint)
    print(len(waypoints))
    return waypoints

def combinations_waypoints(source,destination,preferences):
    waypoints=getwaypoints(source,destination,preferences)
    ini_len=len(waypoints)
    waypoints=waypoints+waypoints
    comb=[]
    for i in range(0,ini_len):
        comb=comb+list(itertools.product(*waypoints[i:i+ini_len]))
    print(len(comb))
    return comb

def find_distance(wp1,wp2):
    if(Distance.objects.filter(waypoint1_waypoint2= wp1+'-'+wp2).exists()):
        return Distance.objects.filter(waypoint1_waypoint2= wp1+'-'+wp2)[0].distance_m
    elif(Distance.objects.filter(waypoint1_waypoint2= wp2+'-'+wp1).exists()):
        return Distance.objects.filter(waypoint1_waypoint2= wp2+'-'+wp1)[0].distance_m
    else:
        print("Calculating dist between "+wp1+"-"+wp2)
        return calc_distance(wp1,wp2)

def calc_distance(waypoint1,waypoint2):
    gmaps = googlemaps.Client(key="AIzaSyCV8CpdE2Zcfz4DoF45-fbgqAuil25ooQI")
    try:
        route = gmaps.distance_matrix(origins=[waypoint1],destinations=[waypoint2],mode="driving",language="English",units="metric")
        distance = route["rows"][0]["elements"][0]["distance"]["value"]
        print(distance,waypoint1,waypoint2)
    except Exception as e:
        print("Error with finding the route between %s and %s." % (waypoint1, waypoint2))
        return -1
    Distance.objects.create(waypoint1_waypoint2=waypoint1+'-'+waypoint2,distance_m=distance).save()
    return distance

def create_dict():
    for i in Distance.objects.all():
        distance[i.waypoint1_waypoint2]=i.distance_m

def find_path(source,destination,combinations):
    min_dist=9999999
    for combination in combinations:
        total_dist=find_distance(source,combination[0])
        for i in range(0,len(combination)-1):
            if (find_distance(combination[i],combination[i+1])) == -1 :
                print(combination[i],combination[i+1])
                break
            total_dist=total_dist+find_distance(combination[i],combination[i+1])
        if (find_distance(combination[i],destination)) != -1 :
            total_dist=total_dist+find_distance(combination[i],destination)
            if(total_dist < min_dist):
                min_dist=total_dist
                way=list(combination)
        else:
            continue
    print(way)
    last.append(way)
    return way

def thread_create(source,destination,preferences):
    start=time.time()
    combinations=combinations_waypoints(source,destination,preferences)
    lst_thread=[]
    l=len(combinations)
    for i in range(0,l,bucket_size):
        args_t=list(combinations[i:min(l,i+bucket_size)])
        locals()['thread'+ str(i)]=threading.Thread(target=find_path,args=(source,destination,args_t))
        lst_thread.append(locals()['thread'+ str(i)])
        
    for thread in lst_thread:
        thread.start()
    for thread in lst_thread:
        thread.join()

    print(len(last))
    final=find_path(source,destination,last)
    print("FINAL",final)
    end=time.time()
    print("TOTAL TIME TAKEN " , end-start)
    return [source]+final+[destination]