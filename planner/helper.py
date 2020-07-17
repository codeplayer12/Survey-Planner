from .models import Camera,SurveyType, Drone, BudgetItem,Department,BudgetItemCost,DepartmentCost,BudgetEstimate
from math import atan,degrees,radians,tan,sqrt,ceil
import logging
import json  

class BudgetCalculations(object):

    def __init__(self, num_flights, images_captured):
        self.num_flights = num_flights
        self.images_captured = images_captured

    def get_total_cost(self):
        departments = Department.objects.all()
        budget_estimate = 0.0
        for department in departments:
            budget_estimate += self.department_total_cost(department)
        budget_estimate_updated = BudgetEstimate.objects.all()[0]   
        budget_estimate_updated.cost =  budget_estimate
        budget_estimate_updated.save()
        print('The total cost '+str(budget_estimate))    
        return budget_estimate

    def item_cost(self):
        list_item = BudgetItem.objects.all()
        cost = {}
        for item in list_item:
           cost.update({item.name:item.total_cost})
        return(cost)

    def department_total_cost(self, department):
       list_budget_items=BudgetItem.objects.filter(department_id=department.id)  
       department_total_cost = 0.0
       for budget_item in list_budget_items:
            budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0]
            department_total_cost += float(budget_item_cost.totalCost)
       
    # Save new department total cost
       updated_department = DepartmentCost.objects.filter(department=department)[0]
       updated_department.total_Cost = department_total_cost
       updated_department.save()
       print("Department : "+department.name +" Total cost : "+str(department_total_cost))
    #    print(dep)
       return department_total_cost


    def set_days(self):
        budget_items = BudgetItem.objects.all()
        total_number_of_images_captured = float(self.images_captured)
        number_of_flights = float(self.num_flights)
        print('Num of captures '+str(total_number_of_images_captured))
        print('Num of flights '+str(number_of_flights))
        ground_s = 0.0
        d_units = 0.0
        ground_units = 0.0
        project_units = 0.0
        # i_support = ceil((number_of_flights/4)*0.2)
        i_support = self.round_up(number_of_flights/4, decimals=0)*0.2
        d_pilots = self.round_up(number_of_flights/4, decimals=0)*1.2
        print('D pilots '+str(d_pilots))
        project_manager = self.round_up(d_pilots/3, decimals=1)
        gis = ceil((((13/600)*total_number_of_images_captured)+((13/600)*total_number_of_images_captured)+(0.1*(13/600)*total_number_of_images_captured)/4)/24)
        drone_r =  d_pilots
        laptop_r = ground_s+d_pilots+gis
       
        local_acc= ground_s+d_pilots+gis        

        for budget_item in budget_items:
            if budget_item.name == "International support": 
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.days=i_support
                budget_item_cost.save()                    
            if budget_item.name == "Drone Pilots":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0]
                d_units = budget_item_cost.units
                budget_item_cost.days= d_pilots
                budget_item_cost.save()                
            if budget_item.name == "Data Gis specialist": 
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.days= gis
                budget_item_cost.save()        
            if budget_item.name =="Ground Survey": 
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                ground_units = budget_item_cost.units
                budget_item_cost.days= 0.0
                budget_item_cost.save()                        
            if budget_item.name =="Project Manager":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                project_units = budget_item_cost.units
                budget_item_cost.days= project_manager
                budget_item_cost.save()                  
            if budget_item.name =="Drone Rental":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.days= drone_r
                budget_item_cost.save()                   
            if budget_item.name =="Laptop Rental":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.days= laptop_r
                budget_item_cost.save()                  
            if budget_item.name =="Organize flight permissions":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.days= 3.0
                budget_item_cost.save()                
            if budget_item.name =="Local Travel":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                local_travel= (ground_s*ground_units)+(d_pilots*d_units)+(project_manager*project_units)
                budget_item_cost.days= local_travel
                budget_item_cost.save()                 
            if budget_item.name =="Local accomodation and per diem":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.days= local_acc
                budget_item_cost.save()                
            if budget_item.name =="Community engagement":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.days= 1.0
                budget_item_cost.save()  
      

    def calculate_budget_item_cost(self):

        budget_items = BudgetItem.objects.all()
        ground_survey_budget_item = BudgetItem.objects.get(name='Ground Survey')
        ground_survey_cost_item = BudgetItemCost.objects.filter(budget_item=ground_survey_budget_item)[0]
        ground_survey_cost_item.totalCost = Calculations.sum(float(ground_survey_cost_item.days),
        float(ground_survey_cost_item.units), float(ground_survey_cost_item.unitCost))
        ground_survey_cost_item.save()
      
        # International Support
        international_budget_item = BudgetItem.objects.get(name='International support')
        international_cost_item = BudgetItemCost.objects.filter(budget_item=international_budget_item)[0]
        international_cost_item.totalCost = Calculations.sum(float(international_cost_item.days),
        float(international_cost_item.units), float(international_cost_item.unitCost))
        international_cost_item.save()
    
        # # Project Manager
        project_manager_budget_item = BudgetItem.objects.get(name='Project Manager')
        project_manager_cost_item = BudgetItemCost.objects.filter(budget_item=project_manager_budget_item)[0]
        project_manager_cost_item.totalCost = Calculations.sum(float(project_manager_cost_item.days),
        float(project_manager_cost_item.units), float(project_manager_cost_item.unitCost))
        project_manager_cost_item.save() # error being shown
        # print(project_m_cost_item)

        # # Drone Pilots
        drone_pilots_budget_item = BudgetItem.objects.get(name='Drone Pilots')
        drone_pilots_cost_item = BudgetItemCost.objects.filter(budget_item=drone_pilots_budget_item)[0]
        drone_pilots_cost_item.totalCost = Calculations.sum(float(drone_pilots_cost_item.days),
        float(drone_pilots_cost_item.units), float(drone_pilots_cost_item.unitCost))
        drone_pilots_cost_item.save()

        # # Data/GIS Specialist
        data_budget_item = BudgetItem.objects.get(name='Data Gis specialist')
        data_cost_item = BudgetItemCost.objects.filter(budget_item=data_budget_item)[0]
        data_cost_item.totalCost = Calculations.sum(float(data_cost_item.days),
        float(data_cost_item.units), float(data_cost_item.unitCost))
        data_cost_item.save()

        # # Drone Rental
        drone_rental_budget_item = BudgetItem.objects.get(name='Drone Rental')
        drone_rental = BudgetItemCost.objects.filter(budget_item=drone_rental_budget_item)[0]
        drone_rental.totalCost = Calculations.sum(float(drone_rental.days),
        float(drone_rental.units), float(drone_rental.unitCost))
        drone_rental.save()

        # # Laptop Rental
        laptop_budget_item = BudgetItem.objects.get(name='Laptop Rental')
        laptop_budget = BudgetItemCost.objects.filter(budget_item=laptop_budget_item)[0]
        laptop_budget.totalCost = Calculations.sum(float(laptop_budget.days),
        float(laptop_budget.units), float(laptop_budget.unitCost))
        laptop_budget.save()

        # # Software Rental
        software_budget_item = BudgetItem.objects.get(name='Software Rental')
        software_budget = BudgetItemCost.objects.filter(budget_item=software_budget_item)[0]
        software_budget.totalCost = Calculations.sum(float(software_budget.units),float(software_budget.unitCost))
        software_budget.save()

        # # Organize flight permissions
        organize_budget_item = BudgetItem.objects.get(name='Organize flight permissions')
        organize_budget = BudgetItemCost.objects.filter(budget_item=organize_budget_item)[0]
        organize_budget.totalCost = Calculations.sum(float(organize_budget.days),float(organize_budget.units),
        float(organize_budget.unitCost))
        organize_budget.save()

        # # Local travel
        local_travel_budget_item = BudgetItem.objects.get(name='Local Travel')
        local_travel_budget = BudgetItemCost.objects.filter(budget_item=local_travel_budget_item)[0]
        local_travel_budget.totalCost = Calculations.sum(float(local_travel_budget.days),
        float(local_travel_budget.unitCost))
        local_travel_budget.save()
             
        # # Local accomodation and per diem
        accommodation_budget_item = BudgetItem.objects.get(name='Local accomodation and per diem')
        accommodation_budget= BudgetItemCost.objects.filter(budget_item=accommodation_budget_item)[0]
        accommodation_budget.totalCost = Calculations.sum(float(accommodation_budget.days), 
        float(accommodation_budget.unitCost))
        accommodation_budget.save() # Error no default value on one of the items

        # # Community engagement
        community_budget_item = BudgetItem.objects.get(name='Community engagement')
        community_budget = BudgetItemCost.objects.filter(budget_item=community_budget_item)[0]
        community_budget.totalCost = Calculations.sum(float(community_budget.days),
        float(community_budget.units), float(community_budget.unitCost))
        community_budget.save()

        # # Insurance
        insurance_budget_item = BudgetItem.objects.get(name='Insurance')
        insurance_budget = BudgetItemCost.objects.filter(budget_item=insurance_budget_item)[0]
        insurance_budget.totalCost = Calculations.sum(float(insurance_budget.units), float(insurance_budget.unitCost))
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

        sub_total_cost = BudgetEstimate.objects.get(name='SubTotal')
        sub_total_cost.cost = sub_total
        sub_total_cost.save()
        print('subtotal ')
        print(sub_total)

        project_management_budget_item = BudgetItem.objects.get(name='Project Management')
        project_management_cost = BudgetItemCost.objects.filter(budget_item=project_management_budget_item)[0]
        projectmanagement_per = Calculations.sum(float(project_management_cost.unitCost),float(sub_total))
        project_management_cost.totalCost = projectmanagement_per
        project_management_cost.save()
             
        project_overhead_budget_item = BudgetItem.objects.get(name='Project Overhead')
        project_overhead_cost = BudgetItemCost.objects.filter(budget_item=project_overhead_budget_item)[0]
        project_overhead_per=Calculations.sum(float(project_overhead_cost.unitCost),float(sub_total))
        project_overhead_cost.totalCost = project_overhead_per
        project_overhead_cost.save()
               
        # print("Sum total")
        # sum_total = Calculations.total_sum(float(sub_total),float(projectmanagement_per), float(project_overhead_per))
        # estimate = Department.objects.get('Other')

    def get_budget_item_cost(self,units,unit_cost):
        return units*unit_cost

    def get_days(self,num_flights,num_images):
        pass

    def set_defaults(self):
        budget_items = BudgetItem.objects.all()
        for budget_item in budget_items:
            if budget_item.name == "International support": 
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.units= 1.0
                budget_item_cost.unitCost= 700.0
                budget_item_cost.totalCost= 140.0
                budget_item_cost.days= 0.2
                budget_item_cost.save()                    
            if budget_item.name == "Drone Pilots":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0]
                budget_item_cost.units= 2.0
                budget_item_cost.unitCost= 200.0
                budget_item_cost.totalCost= 480.0
                budget_item_cost.days= 1.2
                budget_item_cost.save()                
            if budget_item.name == "Data Gis specialist": 
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.units= 1.0
                budget_item_cost.unitCost= 200.0
                budget_item_cost.totalCost= 200.0
                budget_item_cost.days= 1.0
                budget_item_cost.save()        
            if budget_item.name =="Ground Survey": 
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.units= 0.0
                budget_item_cost.unitCost= 400.0
                budget_item_cost.totalCost= 0.0
                budget_item_cost.days= 0.0
                budget_item_cost.save()                      
            if budget_item.name =="Project Manager":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.units= 1.0
                budget_item_cost.unitCost= 350.0
                budget_item_cost.totalCost= 140.0
                budget_item_cost.days= 0.4
                budget_item_cost.save()                
            if budget_item.name =="Drone Rental":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.units= 1.0
                budget_item_cost.unitCost= 500.0
                budget_item_cost.totalCost= 600.0
                budget_item_cost.days= 1.2
                budget_item_cost.save()                   
            if budget_item.name =="Laptop Rental":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.units= 1.0
                budget_item_cost.unitCost= 100.0
                budget_item_cost.totalCost= 220.0
                budget_item_cost.days= 2.2
                budget_item_cost.save()                  
            if budget_item.name =="Organize flight permissions":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.units= 1.0
                budget_item_cost.unitCost= 200.0
                budget_item_cost.totalCost= 600.0
                budget_item_cost.days= 3.0
                budget_item_cost.save()                
            if budget_item.name =="Local Travel":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.unitCost= 50.0
                budget_item_cost.totalCost= 140.0
                budget_item_cost.days= 2.8
                budget_item_cost.save()               
            if budget_item.name =="Local accomodation and per diem":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.unitCost= 40.0
                budget_item_cost.totalCost= 0.0
                budget_item_cost.days= 2.2
                budget_item_cost.save()               
            if budget_item.name =="Community engagement":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.units= 2.0
                budget_item_cost.unitCost= 500.0
                budget_item_cost.totalCost= 1000.0
                budget_item_cost.days= 1.0
                budget_item_cost.save() 
            if budget_item.name =="Software Rental":
                budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0] 
                budget_item_cost.unitCost= 350.0
                budget_item_cost.totalCost= 350.0
                budget_item_cost.units= 1.0
                budget_item_cost.save()       
    

    def round_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return ceil(n * multiplier) / multiplier

    
class Calculations(object):

    def __init__(self,camera_id,survey_type_id,bttry_capacity,flight_height,take_of_area_distance,area_size,distance_travelled_per_flight,size,units,drone_id):
        # super().__init__()
        self.camera_id = camera_id
        self.survey_type_id = survey_type_id
        self.bttry_capacity = bttry_capacity
        self.flight_height = flight_height
        self.take_of_area_distance = take_of_area_distance
        self.area_size = area_size # Assumption that it is already in square meters
        self.distance_travelled_per_flight = distance_travelled_per_flight # Assumption that it is already in meters
        self.size = size
        self.units = units
        self.drone_id = drone_id

        # Set received values for Camera and SurveyType
        self.set_camera_details()
        self.set_survey_type_details()  
        
    def __str__(self):
        return "Camera id" +str(self.camera_id)+ "Survey id "+str(self.survey_type_id)+"Battery"+str(self.bttry_capacity)

    def set_camera_details(self):   
        # Set these values using the received camera id
        selected_camera = Camera.objects.get(pk=self.camera_id)
        if(selected_camera):
            self.focal_length  = selected_camera.lensFocal
            self.lat_dimension_of_sensor_px = selected_camera.pixelw
            self.fwd_dimension_of_sensor_px = selected_camera.pixelh  
            self.lat_dimension_of_sensor_mm = selected_camera.sensorw
            self.fwd_dimension_of_sensor_mm = selected_camera.sensorh   
            self.image_size = selected_camera.imageSize        

    def set_survey_type_details(self):
        # Set these values using the received survey type id
        selected_survey = SurveyType.objects.get(pk=self.survey_type_id)
        if(selected_survey):
            self.lateral_image_overlap = selected_survey.lateral
            self.forward_image_overlap = selected_survey.forward          

    def get_focal_length(self):            
        return self.focal_length/1000

    def get_focal_length_of_lens_mm(self):
        return self.get_focal_length() * 1000

    def get_d_two_f_lateral(self):
        return self.lat_dimension_of_sensor_mm/(2*self.get_focal_length_of_lens_mm())
    
    def get_d_two_f_forward(self):
        return self.fwd_dimension_of_sensor_mm/(2*self.get_focal_length_of_lens_mm())

    def get_radians_lateral(self):
        return 2*atan(self.get_d_two_f_lateral())

    def get_radians_forward(self):
        return 2*atan(self.get_d_two_f_forward())

    def get_angle_of_view_degrees_lateral(self):
        return degrees(self.get_radians_lateral())

    def get_angle_of_view_degrees_forward(self):
        return degrees(self.get_radians_forward())    

    def get_image_ground_coverage_m_lateral(self):
        return (tan(self.get_radians_lateral()/2)* self.flight_height)*2

    def get_image_ground_coverage_m_forward(self):
        return (tan(self.get_radians_forward()/2)*self.flight_height)*2

    def get_pixel_ground_coverage_cm_lateral(self):
        return (self.get_image_ground_coverage_m_lateral()/self.lat_dimension_of_sensor_px)*100
            
    def get_pixel_ground_coverage_cm_forward(self):
        return (self.get_image_ground_coverage_m_forward()/self.fwd_dimension_of_sensor_px)*100

    def get_image_spacing_lateral(self):
        return  (1-self.lateral_image_overlap/100)* self.get_image_ground_coverage_m_lateral()

    def get_image_spacing_forward(self):
        return  (1-self.forward_image_overlap/100)* self.get_image_ground_coverage_m_forward()
  
    def get_polygon(self):
        return sqrt(self.area_size)

    def get_line_spacing(self):
        return self.get_image_spacing_lateral()

    def get_num_of_lines(self):
        return ceil(self.get_polygon()/self.get_line_spacing())

    def get_turn_distance(self):
        return 3.14*0.5*sqrt(self.area_size)

    def get_line_distance(self):
        return (self.get_polygon()*self.get_polygon())/self.get_line_spacing()

    def get_total_distance_covered(self):
        return self.get_turn_distance() + self.get_line_distance()

    def get_f_thirteen(self):
        return ceil(self.get_total_distance_covered()/self.distance_travelled_per_flight)* (self.take_of_area_distance +sqrt(2*self.get_polygon()/1000))*1000*2+self.get_total_distance_covered()
  
    def get_h_thirteen(self):
        return sqrt(2*self.get_polygon())

    def get_num_photos_per_line(self):
        return ceil(self.get_polygon()/self.get_image_spacing_forward())

    def get_total_num_of_photos(self):
        return self.get_num_photos_per_line()* self.get_num_of_lines()

    def get_num_of_gigapixels(self):
        return round((self.get_total_num_of_photos()* self.lat_dimension_of_sensor_px* self.fwd_dimension_of_sensor_px)/(10**9),1)
     
    def get_number_of_flights(self):
        return ceil(self.get_f_thirteen()/self.distance_travelled_per_flight)

    #Processing information sheet
    def estimated_file_size(self):
        return round((4/650)*self.get_total_num_of_photos(),2)

    def per_image(self):
        return round(self.image_size/2,2)    
 
    def get_planner_display_values(self):
        orthophoto_resolution = round((self.get_pixel_ground_coverage_cm_lateral()+self.get_pixel_ground_coverage_cm_lateral())/2,1)
        dsm_resolution = round(self.get_pixel_ground_coverage_cm_lateral()*2,1)
        total_number_of_images_captured = self.get_total_num_of_photos()
        number_of_gigapixels = self.get_num_of_gigapixels()
        number_of_flights = self.get_number_of_flights()
        total_size_of_digital_files = round((total_number_of_images_captured*self.per_image())/1000,1)
        duration_of_mission = ceil(number_of_flights/4)
        area_size = self.area_normal()

        # print("{:.2f}".format(orthophoto_resolution))

        obj = { 
            "num_of_flights":number_of_flights,
            "ortho_reso": orthophoto_resolution,
            "dsm_reso":dsm_resolution,
            "num_images_captured":total_number_of_images_captured,
            "num_gigapixel":number_of_gigapixels,
            "total_digital_files":total_size_of_digital_files,
            "battery_capacity" :self.bttry_capacity,
            "flight_height":self.flight_height ,
            "take_of_area":self.take_of_area_distance ,
            "area_size":area_size , 
            "distance_travelled":self.distance_travelled_per_flight,
            "duration_mission":duration_of_mission,
            "size": self.size,
            "units": self.units,
        }
        return json.dumps(obj)
        # print("Number of flights : "+str(number_of_flights))
        # print("Orthophoto resolution : " +str(orthophoto_resolution))
        # print("DSM resolution : " +str(dsm_resolution))
        # print('Total number of images captured : '+str(total_number_of_images_captured))
        # print('Number of gigapixel : '+ str(number_of_gigapixels))
        # print("pixel ground coverage lateral : "+str(self.get_pixel_ground_coverage_cm_lateral()) +"\n") 
        # + ("pixel ground coverage forward : "+str(self.get_pixel_ground_coverage_cm_forward()))

#    def item_calc_totals(self,day ,unit,unit_cost):
#        total= day*unit*unit_cost
#        return total
    def sum(*args):
        total = 1
        for i in args:
            total *= i
        return ceil(total)
    def total_sum(*args):
        total = 1
        for i in args:
            total += i
        return total

    def area_normal(self):
        if self.units == "meters":
            return self.size/1000000
        elif self.units == "hactares":
            return self.size / 100
        elif self.units == "acres":
            return self.size / 10000
        else:
            return self.size

    # def get_total_cost(*args):
    #     departments = Department.objects.all()
    #     budget_estimate = 0.0
    #     for department in departments:
    #         budget_estimate += department_total_cost(department)
    #     print('The total cost '+str(budget_estimate))    
    #     return budget_estimate    

    # def department_total_cost(self,department):
    #    list_budget_items=BudgetItem.objects.filter(department_id=department.id)  
    #    department_total_cost = 0.0
    #    for budget_item in list_budget_items:
    #         budget_item_cost = BudgetItemCost.objects.filter(budget_item=budget_item)[0]
    #         department_total_cost += budget_item_cost.totalCost
               
    #    print("Department : "+department.name +" Total cost : "+str(department_total_cost))
    #    return department_total_cost