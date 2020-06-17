from .models import Camera,SurveyType
from math import atan,degrees,radians,tan,sqrt,ceil
import logging
import json

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
        # print("Distance travelled per flight constructor : "+str(self.distance_travelled_per_flight))

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
            # print(selected_camera)
            # print("focal length : "+str(self.focal_length))
            # print("lateral dimension of sensor px : "+str(self.lat_dimension_of_sensor_px))  
            # print("forward dimension of sensor px : "+str(self.fwd_dimension_of_sensor_px))           
            # print("lateral dimension of sensor mm : "+str(self.lat_dimension_of_sensor_mm))           
            # print("forward dimension of sensor mm : "+str(self.fwd_dimension_of_sensor_mm))           
         

    def set_survey_type_details(self):
        # Set these values using the received survey type id
        selected_survey = SurveyType.objects.get(pk=self.survey_type_id)
        if(selected_survey):
            self.lateral_image_overlap = selected_survey.lateral
            self.forward_image_overlap = selected_survey.forward
            # print(selected_survey)
            # print("Lateral Image overlap : "+str(self.lateral_image_overlap))
            # print("Forward Image overlap : "+str(self.forward_image_overlap))

    def get_focal_length(self):            
        return self.focal_length/1000

    def get_focal_length_of_lens_mm(self):
        return self.get_focal_length() * 1000

    def get_d_two_f_lateral(self):
        # print('D two f lateral : '+str(self.lat_dimension_of_sensor_mm/(2*self.get_focal_length_of_lens_mm())))
        return self.lat_dimension_of_sensor_mm/(2*self.get_focal_length_of_lens_mm())
    
    def get_d_two_f_forward(self):
        # print('D two f forward : '+str(self.fwd_dimension_of_sensor_mm/(2*self.get_focal_length_of_lens_mm())))
        return self.fwd_dimension_of_sensor_mm/(2*self.get_focal_length_of_lens_mm())

    def get_radians_lateral(self):
        # print("Radian lateral : "+str(2*atan(self.get_d_two_f_lateral())))
        return 2*atan(self.get_d_two_f_lateral())

    def get_radians_forward(self):
        # print("Radian forward : "+str(2*atan(self.get_d_two_f_forward())))
        return 2*atan(self.get_d_two_f_forward())

    def get_angle_of_view_degrees_lateral(self):
        return degrees(self.get_radians_lateral())

    def get_angle_of_view_degrees_forward(self):
        return degrees(self.get_radians_forward())    

    def get_image_ground_coverage_m_lateral(self):
        # print('image ground coverage lateral : '+str((tan(self.get_radians_lateral()/2)* self.flight_height)*2))
        return (tan(self.get_radians_lateral()/2)* self.flight_height)*2

    def get_image_ground_coverage_m_forward(self):
        # print('image ground coverage forward : '+str((tan(self.get_radians_forward()/2)*self.flight_height)*2))
        return (tan(self.get_radians_forward()/2)*self.flight_height)*2

    def get_pixel_ground_coverage_cm_lateral(self):
        # print("Pixel Ground Coverage : "+str((self.get_image_ground_coverage_m_lateral()/self.lat_dimension_of_sensor_px)*100))
        return (self.get_image_ground_coverage_m_lateral()/self.lat_dimension_of_sensor_px)*100
            
    def get_pixel_ground_coverage_cm_forward(self):
        return (self.get_image_ground_coverage_m_forward()/self.fwd_dimension_of_sensor_px)*100

    def get_image_spacing_lateral(self):
        return  (1-self.lateral_image_overlap/100)* self.get_image_ground_coverage_m_lateral()

    def get_image_spacing_forward(self):
        # print("Image spacing forward : "+str((1-self.forward_image_overlap/100)* self.get_image_ground_coverage_m_forward()))
        return  (1-self.forward_image_overlap/100)* self.get_image_ground_coverage_m_forward()
  
    def get_polygon(self):
        return sqrt(self.area_size)

    def get_line_spacing(self):
        return self.get_image_spacing_lateral()

    def get_num_of_lines(self):
        # print(" Polygon : "+ str(self.get_polygon()))
        # print("Line spacing : "+str(self.get_line_spacing()))
        return ceil(self.get_polygon()/self.get_line_spacing())

    def get_turn_distance(self):
        return 3.14*0.5*sqrt(self.area_size)

    def get_line_distance(self):
        return (self.get_polygon()*self.get_polygon())/self.get_line_spacing()

    def get_total_distance_covered(self):
        return self.get_turn_distance() + self.get_line_distance()

    def get_f_thirteen(self):
        # print("total distance covered "+ str(self.get_total_distance_covered()))
        # print("total distance travelled per fight "+ str(self.distance_travelled_per_flight))
        # print("Take of area distance "+ str(self.take_of_area_distance))
        # print("sqrt polygon "+ str(sqrt(2*self.get_polygon()/1000)))
        return ceil(self.get_total_distance_covered()/self.distance_travelled_per_flight)* (self.take_of_area_distance +sqrt(2*self.get_polygon()/1000))*1000*2+self.get_total_distance_covered()
  
    def get_h_thirteen(self):
        return sqrt(2*self.get_polygon())

    def get_num_photos_per_line(self):
        return ceil(self.get_polygon()/self.get_image_spacing_forward())

    def get_total_num_of_photos(self):
        # print("Number of lines : " + str(self.get_num_of_lines()))
        return self.get_num_photos_per_line()* self.get_num_of_lines()

    def get_num_of_gigapixels(self):
        return round((self.get_total_num_of_photos()* self.lat_dimension_of_sensor_px* self.fwd_dimension_of_sensor_px)/(10**9),1)
     
    def get_number_of_flights(self):
        return round(self.get_f_thirteen()/self.distance_travelled_per_flight,0)
 
    def get_planner_display_values(self):
        orthophoto_resolution = round((self.get_pixel_ground_coverage_cm_lateral()+self.get_pixel_ground_coverage_cm_lateral())/2,1)
        dsm_resolution = round(self.get_pixel_ground_coverage_cm_lateral()*2,1)
        total_number_of_images_captured = self.get_total_num_of_photos()
        number_of_gigapixels = self.get_num_of_gigapixels()
        number_of_flights = self.get_number_of_flights()
        # print("{:.2f}".format(orthophoto_resolution))

        obj = { 
            "num_of_flights ":number_of_flights,
            "ortho_reso": orthophoto_resolution,
            "dsm_reso ":dsm_resolution,
            "num_images_captured":total_number_of_images_captured,
            "num_gigapixel":number_of_gigapixels
        }
        return json.dumps(obj)
        # print("Number of flights : "+str(number_of_flights))
        # print("Orthophoto resolution : " +str(orthophoto_resolution))
        # print("DSM resolution : " +str(dsm_resolution))
        # print('Total number of images captured : '+str(total_number_of_images_captured))
        # print('Number of gigapixel : '+ str(number_of_gigapixels))
        # print("pixel ground coverage lateral : "+str(self.get_pixel_ground_coverage_cm_lateral()) +"\n") 
        # + ("pixel ground coverage forward : "+str(self.get_pixel_ground_coverage_cm_forward()))