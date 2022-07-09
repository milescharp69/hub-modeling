import quantities as pq
from Port import Port
class VehicleClass:
    def __init__(self, Veh_Class, mi_kWH, mi_year, className):
        self.Veh_Class = Veh_Class
        self.mi_kWH = mi_kWH
        self.mi_year = mi_year
        self.className = className

    def consumption(self):
        """
        Weekly Consumption of Energy
        :return:
        """
        return (self.mi_year * (1 / self.mi_kWH)).rescale('(kW * hour) / week') * pq.week

    def dwell(self, port):
        """
        Time needed to charge the vehicle using the given port
        :param port:
        :return:
        """
        return self.consumption() / port.Port_kW

    def info(self):
        print(self.className)
        print("Miles per year:", self.mi_year)
        print("Miles Per kWh:", self.mi_kWH)
        print("Weeky consumption:", self.consumption())
        print("0-100% of Weekly Consumption on each Port")
        print("1000kW Port:", self.dwell(Port(pq.Quantity(1000, 'kW'))))
        print("350kW Port:", self.dwell(Port(pq.Quantity(350, 'kW'))))
        print("300kW Port:", self.dwell(Port(pq.Quantity(300, 'kW'))))
        print("150kW Port:", self.dwell(Port(pq.Quantity(150, 'kW'))))

# Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / (kW * hour)') , pq.Quantity(48750, 'miles / year'), 'Class 7-8')
# #print( (Class_C.Dwell_Time(Port(pq.Quantity(150, 'kW')))).rescale("hour/month")  )
# #
# #
# # print()
# # print( (Class_A.Dwell_Time(Port(pq.Quantity(150, 'kW')))).rescale("minute/month")  )
#
Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / (kW * hour)') , pq.Quantity(15638, 'miles / year'), "Class 1-2")
Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / (kW * hour)') , pq.Quantity(16200, 'miles / year'), 'Class 3-6')
Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / (kW * hour)') , pq.Quantity(48750, 'miles / year'), 'Class 7-8')

#print(Class_C.consumption())
# print(Class_C.Dwell_Time(Port(pq.Quantity(150, 'kW'))))
# print(Class_C.dwell(Port(pq.Quantity(150, 'kW'))))
# print(Class_C.dwell(Port(pq.Quantity(350, 'kW'))))
# print(Class_C.dwell(Port(pq.Quantity(1000, 'kW'))))
# print(Class_C.dwell(Port(pq.Quantity(3500, 'kW'))))

Class_A.info()
Class_B.info()
Class_C.info()