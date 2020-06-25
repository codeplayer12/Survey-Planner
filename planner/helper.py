from .models import Camera,SurveyType, Drone, BudgetItem,Department
from math import atan,degrees,radians,tan,sqrt,ceil
import logging
import json  

class BudgetCalculations(object):

    def __init__(self,num_flights,images_captured):
        self.num_flights = num_flights
        self.images_captured = images_captured

# Load all objects and update days if Post form budget calculator, unit cost, days, units
# these can be dictionaries, item name : value pairs, differentiated by dictionary type
# append days for items that have days which can be changed
# calculate budget item cost using values entered by user
# calculate department cost
# calculate budget estimate
#

# if post is get
# Load all objects
# First process calculate days
# calculate budget item cost using default values 
# calculate department cost
# calculate budget estimate
    def get_total_cost(self):
        departments = Department.objects.all()
        budget_estimate = 0.0
        for department in departments:
            budget_estimate += self.department_total_cost(department)
        return budget_estimate

    def item_cost(self):
        list_item = BudgetItem.objects.all()
        cost = {}
        for item in list_item:
           cost.update({item.name:item.total_cost})
        return(cost)



    def department_total_cost(self,department):
       list_budget_items = BudgetItem.objects.filter(department_id= department.id)  
       department_total_cost = 0.0
       dep = {}
       for budget_item in list_budget_items:
            department_total_cost += budget_item.total_cost

            dep.update({budget_item.name: department_total_cost})
       
       print("Department : "+department.name +" Total cost : "+str(department_total_cost))
    #    print(dep)
       return department_total_cost


    def get_days(self):
        budget_items = BudgetItem.objects.all()
        total_number_of_images_captured = self.get_total_num_of_photos()
        number_of_flights = self.get_number_of_flights()
        i_support = ceil((number_of_flights/4)*0.2)
        d_pilots = ceil((number_of_flights/4)*1.2)
        project_manager = d_pilots/3
        gis = ceil((((13/600)*total_number_of_images_captured)+((13/600)*total_number_of_images_captured)+(0.1*(13/600)*total_number_of_images_captured)/4)/24)
        drone_r =  d_pilots
        laptop_r = ground_s+d_pilots+gis
        local_travel= (ground_s*units)+(d_pilots*units)+(project_manager*units)
        local_acc= groung_s+d_pilots+gis
        print(budget_item.name)
        budget_days = {}
        for budget_item in budget_items:
            if budget_item.name =="International Support" :        
                budget_days.update({budget_item.name:i_support})
            if budget_item.name =="Drone pilot":
                budget_days.update({budget_item.name:d_pilots})
            if budget_item.name =="Data Gis specialist":               
                budget_days.update({budget_item.name:gis})
            if budget_item.name =="Ground Survey":            
                budget_days.update({budget_item.name:0})
            if budget_item.name =="Project Manager":
                budget_days.update({budget_item.name:project_manager})
            if budget_item.name =="Drone Rental":
                budget_days.update({budget_item.name:drone_r})    
            if budget_item.name =="Laptop Rental":
                budget_days.update({budget_item.name:laptop_r})   
            if budget_item.name =="Organize flight permissions":
                budget_days.update({budget_item.name:3}) 
            if budget_item.name =="Local Travel":
                budget_days.update({budget_item.name:local_travel}) 
            if budget_item.name =="Local accomodation and per diem":
                budget_days.update({budget_item.name:local_acc}) 
            if budget_item.name =="Community engagement":
                budget_days.update({budget_item.name:1})

        return budget_days

    def get_budget_item_cost(self,days,units,unit_cost):
        return days*units*unit_cost

    def get_budget_item_cost(self,units,unit_cost):
        return units*unit_cost

    def get_days(self,num_flights,num_images):
        pass

    
class Calculations(object):

    def __init__(self,camera_id,survey_type_id,bttry_capacity,flight_height,take_of_area_distance,area_size,distance_travelled_per_flight):
        # super().__init__()
        self.camera_id = camera_id
        self.survey_type_id = survey_type_id
        self.bttry_capacity = bttry_capacity
        self.flight_height = flight_height
        self.take_of_area_distance = take_of_area_distance
        self.area_size = area_size # Assumption that it is already in square meters
        self.distance_travelled_per_flight = distance_travelled_per_flight # Assumption that it is already in meters

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
            "area_size":self.area_size , 
            "distance_travelled":self.distance_travelled_per_flight,
            "duration_mission":duration_of_mission
        }
        return json.dumps(obj)
        # print("Number of flights : "+str(number_of_flights))
        # print("Orthophoto resolution : " +str(orthophoto_resolution))
        # print("DSM resolution : " +str(dsm_resolution))
        # print('Total number of images captured : '+str(total_number_of_images_captured))
        # print('Number of gigapixel : '+ str(number_of_gigapixels))
        # print("pixel ground coverage lateral : "+str(self.get_pixel_ground_coverage_cm_lateral()) +"\n") 
        # + ("pixel ground coverage forward : "+str(self.get_pixel_ground_coverage_cm_forward()))

   