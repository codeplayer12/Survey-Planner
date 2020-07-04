from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .helper import Calculations, BudgetCalculations
from django.urls import reverse
from .models import Camera, Drone, SurveyType, BudgetItem, BudgetEstimate
import json
from django.core import serializers
import requests

# Create your views here.
def index(request):

    if request.method == "POST":
        drone_id = request.POST["drone"]
        camera_id = request.POST["camera"]
        survey_type_id = request.POST["survey_select"]
        take_of_area_distance = int(request.POST["take_of_area"])
        area_size = area_calc(int(request.POST["area_size"]), request.POST["units"])
        bttry_capacity = int(request.POST["battery_capacity"])
        flight_height = int(request.POST["flight_height"])

        selected_drone = Drone.objects.get(id=drone_id)
        distance_travelled_per_flight = (
            selected_drone.flightTime * 60 * selected_drone.cruiseSpeed
        ) / (1 + (bttry_capacity / 100) + flight_height * (0.01 / 12.5))
        cal = Calculations(
            camera_id,
            survey_type_id,
            bttry_capacity,
            flight_height,
            take_of_area_distance,
            area_size,
            distance_travelled_per_flight,
        )
        planner_values = json.loads(cal.get_planner_display_values())

        cameras = Camera.objects.all()
        drones = Drone.objects.all()
        surveys = SurveyType.objects.all()

        #    print("Camera id "+str(camera_id))
        #    print(planner_values)

        select_survey = surveys.get(id=survey_type_id)
        select_drone = drones.get(id=drone_id)
        select_camera = cameras.get(id=camera_id)
        budget_estimate = BudgetEstimate.objects.all()[0]
        print(budget_estimate)
        return render(
            request,
            "planner/index.html",
            {
                "planner_values": planner_values,
                "cameras": cameras,
                "drones": drones,
                "surveys": surveys,
                "select_drone": select_drone,
                "select_survey": select_survey,
                "select_camera": select_camera,
                "budget_estimate": budget_estimate
            },
        )
    # except Exception as e:
    #     return HttpResponse( str(e))

    cameras = Camera.objects.all()
    drones = Drone.objects.all()
    surveys = SurveyType.objects.all()

    try:
        # data = json.loads(request.body)
        # # print(data)
        # camera_id = data['camera_id']
        # Load default values
        camera_id = 15
        drone_id = 18
        survey_type_id = 1
        flight_height = 30
        bttry_capacity = 100
        area_size = 1000
        distance_travelled_per_flight = 20988.14
        take_of_area_distance = 5
        select_survey = surveys.get(id=survey_type_id)
        select_drone = drones.get(id=drone_id)
        select_camera = cameras.get(id=camera_id)
        cal = Calculations(
            camera_id,
            survey_type_id,
            bttry_capacity,
            flight_height,
            take_of_area_distance,
            area_size,
            distance_travelled_per_flight,
        )
        planner_values = json.loads(cal.get_planner_display_values())
        budget_estimate = BudgetEstimate.objects.all()[0]
        print("Budget cost "+ str(budget_estimate.cost))
        return render(
            request,
            "planner/index.html",
            {
                "planner_values": planner_values,
                "cameras": cameras,
                "drones": drones,
                "surveys": surveys,
                "select_drone": select_drone,
                "select_survey": select_survey,
                "select_camera": select_camera,
                "budget_estimate": budget_estimate
            },
        )
    except Exception as e:
        return HttpResponse(str(e))


def area_calc(area, unit):
    if unit == "kilometres":
        return area * 1000000
    elif unit == "hectares":
        return area * 100
    elif unit == "acres":
        return area * 10000
    else:
        return area


def get_drone_values(request):
    if request.method == "GET":
        drone_id = request.GET.get("value")
        try:
            drone = Drone.objects.get(id=drone_id)
        except:
            return JsonResponse({"success": False}, status=400)
        data = {"cruise_speed": drone.cruiseSpeed, "flight_time": drone.flightTime, "id":drone.id}
        return JsonResponse({"data": data}, status=200)
    return JsonResponse({"success": False}, status=400)


def get_survey_values(request):
    if request.method == "GET":
        survey_id = request.GET.get("value")
        try:
            survey = SurveyType.objects.get(id=survey_id)
        except:
            return JsonResponse({"success": False}, status=400)
        data = {"forward": survey.forward, "lateral": survey.lateral}
        return JsonResponse({"data": data}, status=200)
    return JsonResponse({"success": False}, status=400)


def budget_calc(request):
    if request.method == "POST":
        num_flights = request.POST["num_flights"]
        images_captured = request.POST["images_captured"] 
        selected_drone_id = request.POST["selected_drone"]

        selected_drone = Drone.objects.get(id=selected_drone_id)
        print(selected_drone)
        print(images_captured)
        print(num_flights)
        # budget_items = BudgetItem.objects.all()
        # budget_items(Insurance)
        # print(budget_items)
        # cal = BudgetCalculations(num_flights, images_captured)
        # total_cost = cal.get_total_cost()
        # print("Total cost " + str(total_cost))
        # cost = cal.item_cost()
        # return render(
            # request, "planner/budget.html", {"budget_items": budget_items, "cost": cost}
        # )
        return render(
            request, "planner/budget.html"
        )
    elif request.method == "GET":
        return render(request, "planner/budget.html")

def budget_adjustment(request):
    if request.method == 'POST':
        # Ground unit values
        ground_days = request.POST["ground_days"]
        ground_unit = request.POST["ground_unit"]
        ground_unit_cost = request.POST["ground_unit_cost"]

        print('Ground days '+str(ground_days)+
        ' Ground unit'+str(ground_unit)+
        ' Ground unit cost '+str(ground_unit_cost))

        # International Support
        # international_days = request.POST["international_days"]
        # international_unit = request.POST["international_unit"]
        # ground_unit_cost = request.POST["international_unit_cost"]

        # # Project Manager
        # project_m_days = request.POST["project_m_days"]
        # project_m_unit = request.POST["project_m_unit"]
        # project_m_unit_cost = request.POST["project_m_unit_cost"]
             
def get_default_values():
    pass
