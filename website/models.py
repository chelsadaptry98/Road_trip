from django.db import models

# Create your models here.

class Waypoints(models.Model):
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=35)
    district=models.CharField(max_length=35)
    class Meta:
        verbose_name_plural = 'Waypoints'
    def __str__(self):
        return self.name

class Distance(models.Model):
    waypoint1_waypoint2=models.CharField(max_length=200)
    distance_m=models.IntegerField()
    class Meta:
        verbose_name_plural = 'Distance'
    def __str__(self):
        return self.waypoint1_waypoint2

