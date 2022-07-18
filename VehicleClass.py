import quantities as pq
from Port import Port

class vehicleClass(object):
    #TODO: Add doc string
    #TODO: Add args** thing/ pop parameters into where they need to go
    def __init__(self, veh_class):
        if veh_class == 0:
            self.mi_kWH = pq.Quantity(3.181, 'miles / (kW * hour)')
            self.mi_year = pq.Quantity(15638, 'miles / year')
            self.className = 'Class 1-2'
        elif veh_class == 1:
            self.mi_kWH = pq.Quantity(1.245, 'miles / (kW * hour)')
            self.mi_year = pq.Quantity(16200, 'miles / year')
            self.className = 'Class 3-6'
        else:
            self.mi_kWH = pq.Quantity(0.41, 'miles / (kW * hour)')
            self.mi_year = pq.Quantity(48750, 'miles / year')
            self.className = 'Class 7-8'

class car(vehicleClass):
    def __init__(self, battery_capacity, vehicle_class):
        super(car, self).__init__(vehicle_class)
        self.battery_capacity = battery_capacity  # Energy Capacity
        self.battery = 0.1 * self.battery_capacity
# #miles / kw*h
# #miles / year -> year
# #
#         # TODO: Add a power curve this is important because the power curve for a given vehicle heavily impacts the "performance" of its charge session
#         #Power curve affects the power rate which in turn affects charge time
#         #if the current capacity >=5%   and <= 40%:
#         self.week_kw_usage_to_be_met = (self.mi_year * (1/self.mi_kWH)).rescale('(kW * hour) / week') * pq.week
#
#         self.start_charge = self.battery * 0.8 # Vehicle is always between 10-90% SOC
#         # TODO: Characterize charging behavior

    def charge(self):
        """
        This method should determine how much energy kW the vehicle needs
        :return: vehicle consumption
        """
        if self.className == 'Class 1-2' or self.className == 'Class 3-6':
            return ((self.mi_year * (1/self.mi_kWH)).rescale('(kW * hour) / week') * pq.week) / 2
        else:
            return ((self.mi_year * (1/self.mi_kWH)).rescale('(kW * hour) / day') * pq.day)

    def charge_time(self, port_used):
        return




'''
13.459737530823492 h*kW/d
35.62580730318138 h*kW/d
325.54408943201827 h*kW/d

Class C vehicles will have to charge once per day 



How much does each vehicle need within a session consumption per day
Class A needs 15%
Class b needs 15%
Class C needs 60%

Dont generated vehicle if there is already a vehicle of that vehicle class still in the queue
Is there a difference between a vehicle being serviced 

'''
