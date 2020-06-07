import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from website.models import Waypoints
from functools import reduce


def district_fetch(waypoints):
  district = []
  for way in waypoints:
    wp=Waypoints.objects.filter(name__iexact=way)
    district.append(wp[0].district)
  return district



def weather_prediction(way):
  d=pd.read_csv('website/training.csv')
  d_test = pd.read_csv('website/testing.csv')
  #print(d_test)
  #print(d)

  feature_cols = ['MeanTemp','Precipitation','DewPoint','Wind','Pressure','Visibility']
  X = d[feature_cols] # Features
  y = d.SuitableForTravelling # Target variable
  x_test = d_test[feature_cols]
  y_test = d_test.SuitableForTravelling

  clf = DecisionTreeClassifier()
  clf = clf.fit(X,y)
  testing = pd.read_csv('website/weather_dataset.csv')

  districts = district_fetch(way)
  print(districts)
  

  # substitute district of the place that is selected to find the favorable months to travel 
  months = []
  for district in districts:
    new = testing.loc[testing['Place'] == district]
    a= []
    X = new[feature_cols]
    y_pred = clf.predict(X)  
    for i in range(len(y_pred)):
      if y_pred[i] == 'Yes' :
        a.append(new['Month'].iloc[i])
    months.append(a)
  favourable_for_travelling = list(reduce(lambda i, j: i & j, (set(x) for x in months)))
  #favourable_for_travelling = set(a)
  print(months)
  print(favourable_for_travelling)
  return  favourable_for_travelling
  # new = testing.loc[testing['Place'] == 'Shimoga']
  # X = new[feature_cols]
  # a = []
  # y_pred = clf.predict(X)
  # for i in range(len(y_pred)):
  #     if y_pred[i] == 'Yes':
  #         a.append(new['Month'].iloc[i])
  # print(a) 

    
