


class MissionManager:

    def __init__(self):
        self.mission_state = 0
        self.base_altitude = 0
        self.last_altitude = 0

    def complete_startup(self):
        if self.mission_state == 0:
            self.mission_state = 1
    
    def complete_transmission(self,rocket_gps,load_gps):
        if self.mission_state == 1 and any(rocket_gps) and any(load_gps):
            self.mission_state = 2

    def complete_liftoff(self,altitude):
        if self.mission_state == 2 and altitude:
            if self.base_altitude:
                if self.base_altitude + 5 < altitude: #TOLERANCE
                    self.mission_state = 3
            else:
                self.base_altitude = altitude

    def complete_deploy(self,rocket_state):
        if self.mission_state == 3 and rocket_state:
            self.mission_state = 4

    def complete_freefall(self,altitude):
        if self.mission_state == 4 and altitude:
            if self.last_altitude:
                if self.last_altitude - 5 > altitude: #TOLERANCE
                    self.mission_state = 5
            else:
                self.last_altitude = altitude
