from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .helper import Calculations, BudgetCalculations
from django.urls import reverse
from .models import Camera, Drone, SurveyType, BudgetItem, BudgetEstimate,BudgetItemCost,DepartmentCost,PlannerValue,AreaSizeAndUnit,Currency       
import json
from django.core import serializers
import requests

# Home 
def home(request):
    # Calculations.home_view() 
    planner_values = PlannerValue.objects.all()[0]   

    cameras = Camera.objects.all()
    drones = Drone.objects.all()
    surveys = SurveyType.objects.all()
    currencies = Currency.objects.all()

    select_survey = surveys.get(id=planner_values.survey_type_id)
    select_drone = drones.get(id=planner_values.drone_id)
    select_camera = cameras.get(id=planner_values.camera_id)
    budget_estimate = BudgetEstimate.objects.get(name='Total')
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
            "budget_estimate": budget_estimate,
            "currencies":currencies
        },
    )
    

# Create your views here.
def index(request):

    if request.method == "POST":
        if "back_button" in request.POST:
            # Request from budget estimate back button
            planner_values = PlannerValue.objects.all()[0]   
            cameras = Camera.objects.all()
            drones = Drone.objects.all()
            surveys = SurveyType.objects.all()
            currencies = Currency.objects.all()
            area_units = AreaSizeAndUnit.objects.all()
            select_survey = surveys.get(id=planner_values.survey_type_id)
            select_drone = drones.get(id=planner_values.drone_id)
            select_camera = cameras.get(id=planner_values.camera_id)
            budget_estimate = BudgetEstimate.objects.get(name='Total')
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
                    "budget_estimate": budget_estimate,
                    "area_units": area_units,
                    "currencies":currencies
                },
            )

        else:
            drone_id = request.POST["drone"]
            camera_id = request.POST["camera"]
            survey_type_id = request.POST["survey_select"]
            take_of_area_distance = float(request.POST["take_of_area"])
            size = int(request.POST["area_size"])
            units = request.POST["units"]
            area_size = area_calc(int(request.POST["area_size"]), request.POST["units"])
            bttry_capacity = float(request.POST["battery_capacity"])
            flight_height = float(request.POST["flight_height"])

            selected_drone = Drone.objects.get(id=drone_id)
            flight_time = 0
            cruise_speed = 0
            if selected_drone.name == 'Custom':
                flight_time = float(request.POST["flight_time"])
                cruise_speed = float(request.POST["cruise_speed"])
                print("Received values are flight time "+str(flight_time)+ " cruise speed "+str(cruise_speed))
                # Save the new custom values to the database so that they can be sent back correctly to the UI
                custom_drone = Drone.objects.get(name='Custom')
                custom_drone.cruiseSpeed = cruise_speed
                custom_drone.flightTime = flight_time
                custom_drone.save()
                print("\n"+"New drone name "+ custom_drone.name + "Cruise speed "+str(custom_drone.cruiseSpeed) +"Flight time"+str(custom_drone.flightTime)+"\n")
                print("Flight time : "+str(flight_time)+ "Cruise Speed : "+str(cruise_speed))
            else:
                flight_time = selected_drone.flightTime
                cruise_speed = selected_drone.cruiseSpeed
            
            #Check if the survey type is Custom and set appropriate values
            selected_survey = SurveyType.objects.get(id=survey_type_id)
            if selected_survey.name == 'Custom':
                forward = float(request.POST["custom_forward"])
                lateral = float(request.POST["custom_lateral"])
                # Save the new custom values to the database so that they can be sent back correctly to the UI
                modifiedSurvey =  SurveyType.objects.get(name='Custom')
                modifiedSurvey.forward=forward
                modifiedSurvey.lateral=lateral
                modifiedSurvey.save()
                # custom_survey.forward = forward
                # custom_survey.lateral = lateral
                # custom_survey.save()
                custom_survey = SurveyType.objects.get(pk=selected_survey.id)
                print("\n"+"New survey name "+ custom_survey.name + "forward "+str(custom_survey.forward) +"lateral"+str(custom_survey.lateral)+"\n")
                print("Forward: " +str(forward)+ "Lateral : " +str(lateral))

            # Calculate distance travelled per flight

            distance_travelled_per_flight = (
                flight_time * 60 * cruise_speed
            ) / (1 + (bttry_capacity / 100) + flight_height * (0.01 / 12.5))

            # Perform non-budget calculations
            cal = Calculations(
                camera_id,
                survey_type_id,
                bttry_capacity,
                flight_height,
                take_of_area_distance,
                area_size,
                distance_travelled_per_flight,
                size,
                units,
                drone_id,
            )

            
            planner_values = json.loads(cal.get_planner_display_values())
            # print(planner_values['num_of_flights'])

            # Calculate days
            cal = BudgetCalculations(planner_values['num_of_flights'], planner_values['num_images_captured'])
            cal.set_days()
            cal.calculate_budget_item_cost()
            cal.get_total_cost()

            cameras = Camera.objects.all()
            drones = Drone.objects.all()
            surveys = SurveyType.objects.all()
            currencies = Currency.objects.all()
            area_units = AreaSizeAndUnit.objects.all()

            select_survey = surveys.get(id=survey_type_id)
            select_drone = drones.get(id=drone_id)
            select_camera = cameras.get(id=camera_id)
            budget_estimate = BudgetEstimate.objects.get(name='Total')
            # print("New Budget "+budget_estimate)
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
                    "budget_estimate": budget_estimate,
                    "area_units": area_units,
                    "currencies":currencies
                },
            )       

    cameras = Camera.objects.all()
    drones = Drone.objects.all()
    surveys = SurveyType.objects.all()
    area_units = AreaSizeAndUnit.objects.all()
    currencies = Currency.objects.all()

    try:
        # data = json.loads(request.body)
        # # print(data)
        # camera_id = data['camera_id']
        # Load default values
        camera_id = 15
        drone_id = 18
        survey_type_id = 1
        flight_height = 80
        bttry_capacity = 30
        size=1
        units='kilometres'
        area_size = 1
        distance_travelled_per_flight = 20988.14
        take_of_area_distance = 0.5
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
            size,units,
            drone_id
        )
        planner_values = json.loads(cal.get_planner_display_values())

        # Set budget default values
        cal = BudgetCalculations(1, 1)
        cal.set_defaults()
        # cal.get_total_cost()
        budget_estimate = BudgetEstimate.objects.filter(name='Total')[0]
        # budget_estimate = BudgetEstimate.objects.all()[0]
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
                "budget_estimate": budget_estimate,
                "area_units": area_units,
                "currencies":currencies
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

        # Get the default values
        budget_item_costs = BudgetItemCost.objects.all()
        department_costs = DepartmentCost.objects.all()
        budget_estimate = BudgetEstimate.objects.get(name='Total')
        budget_sub_total = BudgetEstimate.objects.get(name='SubTotal')

        # budget_items = BudgetItem.objects.all()
        # budget_items(Insurance)
        # print(budget_items)
        cal = BudgetCalculations(num_flights, images_captured)
        cal.set_days()
        # total_cost = cal.get_total_cost()
        # print("Total cost " + str(total_cost))
        # cost = cal.item_cost()
        # return render(
            # request, "planner/budget.html", {"budget_items": budget_items, "cost": cost}
        # )
        return render(
            request, "planner/budget.html"
            ,{
                "budget_item_costs": budget_item_costs,
                "department_costs": department_costs,
                "budget_estimate": budget_estimate,
                "budget_sub_total": budget_sub_total                
        },)
        
    elif request.method == "GET":
        # get all the default values to display
        budget_item_costs = BudgetItemCost.objects.all()
        department_costs = DepartmentCost.objects.all()
        budget_estimate = BudgetEstimate.objects.get(name='Total')
        budget_sub_total = BudgetEstimate.objects.get(name='SubTotal')
        
        return render(request, "planner/budget.html"
        ,{
                "budget_item_costs": budget_item_costs,
                "department_costs": department_costs,
                "budget_estimate": budget_estimate,
                "budget_sub_total": budget_sub_total               
        },)

def budget_adjustment(request):
    if request.method == 'POST':
        # Ground unit values
        ground_days = request.POST["ground_days"]
        ground_unit = request.POST["ground_unit"]
        ground_unit_cost = request.POST["ground_unit_cost"]

        # print('Ground days '+str(ground_days)+
        # ' Ground unit'+str(ground_unit)+
        # ' Ground unit cost '+str(ground_unit_cost))
        # total = Calculations.sum(float(ground_days),float(ground_unit), float(ground_unit_cost))
        # print(total)

        ground_survey_budget_item = BudgetItem.objects.get(name='Ground Survey')
        print('Survey Budget Item')
        print(ground_survey_budget_item)
        print('Unit Cost')
        ground_survey_cost_item = BudgetItemCost.objects.filter(budget_item=ground_survey_budget_item)[0]
        ground_survey_cost_item.days = ground_days
        ground_survey_cost_item.unitCost = ground_unit_cost
        ground_survey_cost_item.units = ground_unit
        ground_survey_cost_item.totalCost = Calculations.sum(float(ground_days),float(ground_unit), float(ground_unit_cost))
        ground_survey_cost_item.save()
        print(ground_survey_cost_item.unitCost)

        # International Support
        international_days = request.POST["international_days"]
        international_unit = request.POST["international_unit"]
        international_unit_cost = request.POST["international_unit_cost"]
        totalCost = Calculations.sum(float(international_days),float(international_unit), float(international_unit_cost))
        print()

        international_budget_item = BudgetItem.objects.get(name='International support')
        international_cost_item = BudgetItemCost.objects.filter(budget_item=international_budget_item)[0]
        print(international_cost_item)
        international_cost_item.days = international_days
        international_cost_item.unitCost = international_unit_cost
        international_cost_item.units = international_unit
        international_cost_item.totalCost = Calculations.sum(float(international_days),float(international_unit), float(international_unit_cost))
        international_cost_item.save()
    
        # # Project Manager
        project_manager_days = request.POST["project_manager_days"]
        project_manager_unit = request.POST["project_manager_unit"]
        project_manager_unit_cost = request.POST["project_manager_unit_cost"]
        # print('work '+project_m_unit+' '+ project_m_unit_cost+ ' '+ project_m_days)

        project_manager_budget_item = BudgetItem.objects.get(name='Project Manager')
        project_manager_cost_item = BudgetItemCost.objects.filter(budget_item=project_manager_budget_item)[0]
        project_manager_cost_item.days = project_manager_days
        project_manager_cost_item.unitCost = project_manager_unit_cost
        project_manager_cost_item.units = project_manager_unit
        project_manager_cost_item.totalCost = Calculations.sum(float(project_manager_days),float(project_manager_unit), float(project_manager_unit_cost))
        project_manager_cost_item.save() # error being shown
        # print(project_m_cost_item)

        # # Drone Pilots
        drone_p_days = request.POST["drone_p_days"]
        drone_p_unit = request.POST["drone_p_unit"]
        drone_p_unit_cost = request.POST["drone_p_unit_cost"]

        drone_pilots_budget_item = BudgetItem.objects.get(name='Drone Pilots')
        drone_pilots_cost_item = BudgetItemCost.objects.filter(budget_item=drone_pilots_budget_item)[0]
        drone_pilots_cost_item.days = drone_p_days
        drone_pilots_cost_item.unitCost = drone_p_unit_cost
        drone_pilots_cost_item.units = drone_p_unit
        drone_pilots_cost_item.totalCost = Calculations.sum(float(drone_p_days),float(drone_p_unit), float(drone_p_unit_cost))
        drone_pilots_cost_item.save()

        # # Data/GIS Specialist
        gis_days = request.POST["gis_days"]
        gis_unit = request.POST["gis_unit"]
        gis_unit_cost = request.POST["gis_unit_cost"]

        data_budget_item = BudgetItem.objects.get(name='Data Gis specialist')
        data_cost_item = BudgetItemCost.objects.filter(budget_item=data_budget_item)[0]
        data_cost_item.days = gis_days
        data_cost_item.unitCost = gis_unit_cost
        data_cost_item.units = gis_unit
        data_cost_item.totalCost = Calculations.sum(float(gis_days),float(gis_unit), float(gis_unit_cost))
        data_cost_item.save()

        # # Drone Rental
        drone_r_days = request.POST["drone_r_days"]
        drone_r_unit = request.POST["drone_r_unit"]
        drone_r_unit_cost = request.POST["drone_r_unit_cost"]

        drone_rental_budget_item = BudgetItem.objects.get(name='Drone Rental')
        drone_rental = BudgetItemCost.objects.filter(budget_item=drone_rental_budget_item)[0]
        drone_rental.days = drone_r_days
        drone_rental.unitCost = drone_r_unit_cost
        drone_rental.units = drone_r_unit
        drone_rental.totalCost = Calculations.sum(float(drone_r_days),float(drone_r_unit), float(drone_r_unit_cost))
        drone_rental.save()

        # # Laptop Rental
        laptop_r_days = request.POST["laptop_r_days"]
        laptop_r_unit = request.POST["laptop_r_unit"]
        laptop_r_unit_cost = request.POST["laptop_r_unit_cost"]
        t1 = Calculations.sum(float(laptop_r_days),float(laptop_r_unit), float(laptop_r_unit_cost))
        print(' -'+ laptop_r_days+' '+laptop_r_unit+' '+laptop_r_unit_cost)
        print(t1)


        laptop_budget_item = BudgetItem.objects.get(name='Laptop Rental')
        laptop_budget = BudgetItemCost.objects.filter(budget_item=laptop_budget_item)[0]
        laptop_budget.days = laptop_r_days
        laptop_budget.unitCost = laptop_r_unit_cost
        laptop_budget.units = laptop_r_unit
        laptop_budget.totalCost = Calculations.sum(float(laptop_r_days),float(laptop_r_unit), float(laptop_r_unit_cost))
        laptop_budget.save()

        # # Software Rental
        software_r_unit = request.POST["software_r_unit"]
        software_r_unit_cost = request.POST["software_r_unit_cost"]

        software_budget_item = BudgetItem.objects.get(name='Software Rental')
        software_budget = BudgetItemCost.objects.filter(budget_item=software_budget_item)[0]
        software_budget.unitCost = software_r_unit_cost
        software_budget.units = software_r_unit
        software_budget.totalCost = Calculations.sum(float(software_r_unit),float(software_r_unit_cost))
        software_budget.save()

        # # Organize flight permissions
        flight_days = request.POST["flight_days"]
        flight_unit = request.POST["flight_unit"]
        flight_unit_cost = request.POST["flight_unit_cost"]

        organize_budget_item = BudgetItem.objects.get(name='Organize flight permissions')
        organize_budget = BudgetItemCost.objects.filter(budget_item=organize_budget_item)[0]
        organize_budget.unitCost = flight_unit_cost
        organize_budget.units = flight_unit 
        organize_budget.totalCost = Calculations.sum(float(flight_days),float(flight_unit), float(flight_unit_cost))
        organize_budget.save()

        # # Local travel
        travel_days = request.POST["travel_days"]
        travel_unit = request.POST["travel_unit"]
        travel_unit_cost = request.POST["travel_unit_cost"]

        local_travel_budget_item = BudgetItem.objects.get(name='Local Travel')
        local_travel_budget = BudgetItemCost.objects.filter(budget_item=local_travel_budget_item)[0]
        local_travel_budget.unitCost = travel_unit_cost
        local_travel_budget.units = travel_unit 
        local_travel_budget.totalCost = Calculations.sum(float(travel_days),float(travel_unit_cost))
        local_travel_budget.save()
             
        # # Local accomodation and per diem
        accodomation_days = request.POST["accodomation_days"]
        accodomation_unit = request.POST["accodomation_unit"]
        accodomation_unit_cost = request.POST["accodomation_unit_cost"]

        accommodation_budget_item = BudgetItem.objects.get(name='Local accomodation and per diem')
        accommodation_budget= BudgetItemCost.objects.filter(budget_item=accommodation_budget_item)[0]
        accommodation_budget.unitCost = accodomation_unit_cost
        accommodation_budget.units = accodomation_unit 
        accommodation_budget.totalCost = Calculations.sum(float(accodomation_days), float(accodomation_unit_cost))
        accommodation_budget.save() # Error no default value on one of the items

        # # Community engagement
        community_days = request.POST["community_days"]
        community_unit = request.POST["community_unit"]
        community_unit_cost = request.POST["community_unit_cost"]

        community_budget_item = BudgetItem.objects.get(name='Community engagement')
        community_budget = BudgetItemCost.objects.filter(budget_item=community_budget_item)[0]
        community_budget.unitCost = community_unit_cost
        community_budget.units = community_unit
        community_budget.totalCost = Calculations.sum(float(community_days),float(community_unit), float(community_unit_cost))
        community_budget.save()

        # # Insurance
        insurance_days = request.POST["insurance_days"]
        insurance_unit = request.POST["insurance_unit"]
        insurance_unit_cost = request.POST["insurance_unit_cost"]

        insurance_budget_item = BudgetItem.objects.get(name='Insurance')
        insurance_budget = BudgetItemCost.objects.filter(budget_item=insurance_budget_item)[0]
        insurance_budget.unitCost = insurance_unit_cost
        insurance_budget.units = insurance_unit
        insurance_budget.totalCost = Calculations.sum(float(insurance_unit), float(insurance_unit_cost))
        insurance_budget.save()

        # Subtotal
        sub_total = Calculations.total_sum(
            ground_survey_cost_item.totalCost,
            international_cost_item.totalCost,
            project_manager_cost_item.totalCost,
            drone_pilots_cost_item.totalCost,
            data_cost_item.totalCost,
            drone_rental.totalCost,
            laptop_budget.totalCost,
            software_budget.totalCost,
            organize_budget.totalCost,
            local_travel_budget.totalCost,
            accommodation_budget.totalCost,
            community_budget.totalCost,
            insurance_budget.totalCost)

        # sub_total_item = BudgetItem.objects.get(name='Subtotal')
        sub_total_cost = BudgetEstimate.objects.get(name='SubTotal')
        sub_total_cost.cost = sub_total
        sub_total_cost.save()
        print('subtotal ')
        print(sub_total)

        # # Project Management 10%
        # project_m_unit = request.POST["project_m_unit"]
        project_m_unit_cost = request.POST["project_m_unit_cost"]
        # convert to percentage before calculation
        project_m_unit_cost = float(project_m_unit_cost)/100
        projectmanagement_per = Calculations.sum(float(project_m_unit_cost),float(sub_total))

        project_management_budget_item = BudgetItem.objects.get(name='Project Management')
        project_management_cost = BudgetItemCost.objects.filter(budget_item=project_management_budget_item)[0]
        project_management_cost.totalCost = projectmanagement_per
        project_management_cost.unitCost = project_m_unit_cost
        project_management_cost.save()
        print("10% of subtotal Project Management")
        print(Calculations.sum(float(project_m_unit_cost),float(sub_total)))
      
        # # Project Overhead 15%
        # project_o_unit = request.POST["project_o_unit"]
        project_o_unit_cost = request.POST["project_o_unit_cost"]
        project_o_unit_cost = float(project_o_unit_cost)/100
        project_overhead_per = Calculations.sum(float(project_o_unit_cost),float(sub_total))

        # Calculations.sum(float(insurance_unit),float(insurance_unit_cost))

        project_overhead_budget_item = BudgetItem.objects.get(name='Project Overhead')
        project_overhead_cost = BudgetItemCost.objects.filter(budget_item=project_overhead_budget_item)[0]
        project_overhead_cost.totalCost = project_overhead_per
        project_management_cost.unitCost = project_o_unit_cost
        project_overhead_cost.save()
        print("5% of subtotal Project Overhead")
        print(Calculations.sum(float(project_o_unit_cost),float(sub_total)))
        # Calculate total before saving default value
        # sum_totals(project_o_unit,  project_o_unit_cost)

        # Ultimate total to save in db
        print("Sum total")
        sum_total = Calculations.total_sum(float(sub_total),float(projectmanagement_per), float(project_overhead_per))
        # estimate = Department.objects.get('Other')

        # budget_estimate.cost = sum_total
        # budget_estimate.save()
        # print(Calculations.total_sum(float(sub_total),float(projectmanagement_per), float(project_overhead_per)))
        # estimate = BudgetEstimate.objects.all()[0]
        # estimate.cost = sum_total
        # estimate.save()
        # total_cost =Calculations.total_sum(float(sub_total),float(projectmanagement_per), float(project_overhead_per))
        # project_overhead_cost = BudgetItemCost.objects.filter(budget_item=project_overhead_budget_item)[0]
        # project_overhead_cost.totalCost = project_overhead_per
        # project_overhead_cost.save()

        calc = BudgetCalculations(1,1)
        print(calc)
        calc.get_total_cost()
        budget_item_costs = BudgetItemCost.objects.all()
        department_costs = DepartmentCost.objects.all()
        budget_estimate = BudgetEstimate.objects.get(name='Total')
        budget_sub_total = BudgetEstimate.objects.get(name='SubTotal')      
        

        return render(request, "planner/budget.html"
        ,{
            "budget_item_costs": budget_item_costs,
            "department_costs":department_costs,
            "budget_estimate": budget_estimate,
            "budget_sub_total":budget_sub_total              
        },)
    else:
        budget_item_costs = BudgetItemCost.objects.all()
        department_costs = DepartmentCost.objects.all()
        budget_estimate = BudgetEstimate.objects.get(name='Total')
        budget_sub_total = BudgetEstimate.objects.get(name='SubTotal')
        return render(request, "planner/budget.html"
        ,{
            "budget_item_costs": budget_item_costs,
            "department_costs": department_costs,
            "budget_estimate": budget_estimate,
            "budget_sub_total": budget_sub_total             
        },)

def get_default_values(request):
    pass

def credits(request):
    return render(request, 'planner/credits.html')

