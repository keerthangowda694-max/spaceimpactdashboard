import requests
from django.http import JsonResponse
from django.shortcuts import render
import datetime


def index(request):
    return render(request,"index.html")


def solar_flare_data(request):
    start_date = request.GET.get('startDate', '')
    end_date = request.GET.get('endDate', '')
    flares = []

    if start_date and end_date:  # Only fetch when both are entered
        api_key = 'TV9hklgiAu7foqCPGpjG2BfM9tCoB8RoAEiBpwgk'
        url = 'https://api.nasa.gov/DONKI/FLR'
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'api_key': api_key
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if isinstance(data, list) and len(data) > 0:
                for item in data:
                    flare = {
                        'classType': item.get('classType', 'N/A'),
                        'sourceLocation': item.get('sourceLocation', 'N/A'),
                        'peakTime': item.get('peakTime', 'N/A'),
                        'link': item.get('link', '#'),
                    }
                    flares.append(flare)
        except Exception:
            flares = []

    return render(request, "solarflare.html", {
        'flares': flares,
        'start_date': start_date,
        'end_date':end_date})


    
def forecast(request):
    # Get city from POST, default to Berlin
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = "Berlin"

    appid = 'dcd9674a7212515ceb1fd0768ab9c732'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    PARAMS = {'q': city, 'appid': appid, 'units': 'metric'}

    # Initialize variables
    description = temp = icon = day = city_name = ''

    try:
        r = requests.get(url=url, params=PARAMS)
        res = r.json()

        # Check if city exists
        if res.get('cod') == 200:
            description = res['weather'][0]['description']
            icon = res['weather'][0]['icon']
            temp = res['main']['temp']
            day = datetime.date.today()
            city_name = res['name']
        else:
            # City not found
            description = "City not found"
            temp = icon = day = city_name = ''
    except Exception as e:
        # API or network error
        description = "Error fetching weather"
        temp = icon = day = city_name = ''

    return render(request, "forecast.html", {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city
    })

def satellitetracker(request):
    # Default satellite: ISS (International Space Station)
    satellite_id = request.GET.get('id', '25544')  # User can enter other NORAD IDs

    url = f'https://api.wheretheiss.at/v1/satellites/{satellite_id}'
    try:
        response = requests.get(url)
        data = response.json()

        if 'error' not in data:
            satellite = {
                'name': data.get('name', 'Unknown'),
                'latitude': round(data.get('latitude', 0), 2),
                'longitude': round(data.get('longitude', 0), 2),
                'altitude': round(data.get('altitude', 0), 2),
                'velocity': round(data.get('velocity', 0), 2),
                'visibility': data.get('visibility', 'unknown'),
            }
        else:
            satellite = None
    except Exception:
        satellite = None

    return render(request, "satellitetracker.html", {
        'satellite': satellite,
        'satellite_id': satellite_id})



def geomagneticimpactzones(request):
    start_date = request.GET.get('startDate', '')
    end_date = request.GET.get('endDate', '')
    api_key = 'TV9hklgiAu7foqCPGpjG2BfM9tCoB8RoAEiBpwgk'

    url = 'https://api.nasa.gov/DONKI/GST'
    impacts=[]
    if start_date and end_date:
        params = {
        'startDate': start_date,
        'endDate': end_date,
        'api_key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()

        impacts = []
        for event in data:
            if "allKpIndex" in event and event["allKpIndex"]:
                kp = round(event["allKpIndex"][0].get("kpIndex", 0), 2)
                
                # Determine impact zone
                if kp < 4:
                    region = "No disturbance — quiet geomagnetic activity"
                elif kp == 4:
                    region = "High latitudes — mild auroras (Canada, Scandinavia)"
                elif 5 <= kp <= 6:
                    region = "High to mid latitudes — visible auroras, radio disturbances"
                elif 7 <= kp <= 8:
                    region = "Mid-latitudes — power, GPS, and satellite issues"
                else:
                    region = "Global impact — severe geomagnetic storm"

                impacts.append({
                    'gstID': event.get('gstID', 'N/A'),
                    'startTime': event.get('startTime', 'N/A'),
                    'kpIndex': kp,
                    'region': region
                })

    except Exception:
        impacts = []

    return render(request, "geomagnetic.html", {
        'impacts': impacts,
        'start_date': start_date,
        'end_date': end_date
    })