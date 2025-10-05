from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index.html"),
   path('solar-flares/', views.solar_flare_data, name='solar_flare_data'),
   path('forecast/',views.forecast,name="forecast"),
   path('satellitetracker/',views.satellitetracker , name="satellitetracker"),
   path('geomagneticimpactzones/',views.geomagneticimpactzones, name="geomagneticimpactzones")

]

