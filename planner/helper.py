from .models import Camera,SurveyType
from math import atan,degrees,radians,tan,sqrt,ceil

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
          
    def setCameraDetails(self):   
        # Set these values using the received camera id
        selected_camera = Camera.objects.get(pk=self.camera_id)
        if(selected_camera):
            self.focal_length  = selected_camera.lensFocal
            self.lat_dimension_of_sensor_px = selected_camera.pixelw
            self.fwd_dimension_of_sensor_px = selected_camera.pixelh  
            self.lat_dimension_of_sensor_mm = selected_camera.sensorw
            self.fwd_dimension_of_sensor_mm = selected_camera.sensorh              

    def setSurveyTypeDetails(self):
        # Set these values using the received survey type id
        selected_survey = SurveyType.objects.get(pk=self.survey_type_id)
        if(selected_survey):
            self.lateral_image_overlap = selected_survey.lateral
            self.forward_image_overlap = selected_survey.forward

    def get_focal_length(self, focal_length):            
        return focal_length/1000

    def get_d_two_f_lateral(self, lat_dimension_of_sensor_mm):
        return lat_dimension_of_sensor_mm/(2*self.get_focal_length())
    
    def get_d_two_f_forward(self,fwd_dimension_of_sensor_mm):
        return fwd_dimension_of_sensor_mm/(2*self.get_focal_length())

    def get_radians_lateral(self):
        return atan(self.get_d_two_f_lateral())

    def get_radians_forward(self):
        return atan(self.get_d_two_f_forward())

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
        return  (1-self.lateral_image_overlap)* self.get_pixel_ground_coverage_cm_lateral()

    def get_image_spacing_forward(self):
        return  (1-self.forward_image_overlap)* self.get_pixel_ground_coverage_cm_forward()
  
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
        return (self.get_total_num_of_photos()* self.lat_dimension_of_sensor_px()* self.fwd_dimension_of_sensor_px)/pow(10,9)

#Processing information sheet
    def estimated_file_size(self):
        return round((4/650)*self.get_total_num_of_photos(),2)

    def estimated_size_per_mb(self):
        selected_camera = Camera.objects.get(pk=self.camera_id)
        if(selected_camera):
            return selected_camera.imageSize

    def per_image(self):
        return round(self.estimated_size_per_mb()/2,2)
     