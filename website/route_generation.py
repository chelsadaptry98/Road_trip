import itertools
import pandas as pd
import googlemaps
from website.models import Waypoints,Distance
import threading
import time

bucket_size=500
last=[]
distance={}

def getwaypoints(source,destination,preferences):
    waypoints=[]
    for preference in preferences:
        waypoint=[]
        wp=Waypoints.objects.filter(category__iexact=preference).exclude(district__iexact=source).exclude(district__iexact=destination)
        for w in wp:
            waypoint.append(w.name)
        waypoints.append(waypoint)
    print("-----ROUTE GENERATION-----")
    print("Number of preferences",len(waypoints))
    return waypoints

def combinations_waypoints(source,destination,preferences):
    waypoints=getwaypoints(source,destination,preferences)
    ini_len=len(waypoints)
    waypoints=waypoints+waypoints
    comb=[]
    for i in range(0,ini_len):
        comb=comb+list(itertools.product(*waypoints[i:i+ini_len]))
    print("Number of combinations",len(comb))
    return comb

def find_distance(wp1,wp2):
    if(wp1+'-'+wp2 in distance.keys()):
        return distance[wp1+'-'+wp2]
    elif(wp2+'-'+wp1 in distance.keys()):
        return distance[wp2+'-'+wp1]
    else:
        print("Calculating dist between "+wp1+"-"+wp2)
        dist=calc_distance(wp1,wp2)
        return dist

def calc_distance(waypoint1,waypoint2):
    gmaps = googlemaps.Client(key="YOUR KEY")
    try:
        route = gmaps.distance_matrix(origins=[waypoint1],destinations=[waypoint2],mode="driving",language="English",units="metric")
        dist = route["rows"][0]["elements"][0]["distance"]["value"]
        print(dist,waypoint1,waypoint2)
    except Exception as e:
        print("Error with finding the route between %s and %s." % (waypoint1, waypoint2))
        return -1
    Distance.objects.create(waypoint1_waypoint2=waypoint1+'-'+waypoint2,distance_m=dist).save()
    global distance
    distance[waypoint1+'-'+waypoint2]=dist
    return dist

def create_dict():
    global distance
    distance={}
    for i in Distance.objects.all():
        distance[i.waypoint1_waypoint2]=i.distance_m
    

def find_path(source,destination,combinations):
    min_dist=9999999
    way=[]
    for combination in combinations:
        total_dist=find_distance(source,combination[0])
        i=0
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
    last.append(way)
    return way

def thread_create(source,destination,preferences):
    start=time.time()
    combinations=combinations_waypoints(source,destination,preferences)
    global last
    last=[]
    create_dict()
    print("Using in thread_create",type(distance),"with length",len(distance))
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

    print("Length after threading",len(last))
    final=find_path(source,destination,last)
    print("FINAL",final)
    end=time.time()
    print("TOTAL TIME TAKEN " , end-start)
    return [source]+final+[destination]