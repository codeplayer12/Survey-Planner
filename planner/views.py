from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .helper import Calculations
from django.urls import reverse
import json

# Create your views here.
def index(request):

    try:
        # data = json.loads(request.body) 
        # # print(data)
        # camera_id = data['camera_id']
        # survey_type_id = data['survey_type_id']
        # flight_height = data['flight_height']
        # bttry_capacity = data['bttry_capacity']
        # area_size = data['area_size']
        # distance_travelled_per_flight =  data['distance_travelled_per_flight']
        # take_of_area_distance = data['take_of_area_distance']
        camera_id = 15
        survey_type_id = 1
        flight_height = 30
        bttry_capacity = 100
        area_size = 1000
        distance_travelled_per_flight =  20988.14 
        take_of_area_distance = 5
        cal = Calculations(camera_id,survey_type_id,bttry_capacity,flight_height,take_of_area_distance,area_size,distance_travelled_per_flight)
        planner_values = cal.get_planner_display_values()    
        # return HttpResponse(planner_values, content_type='application/json') 
        # 
        print(planner_values)
        context = {'planner_values': planner_values}  
        return render(request, 'planner/index.html', context) 
    except Exception as e:
        return HttpResponse( str(e))

    