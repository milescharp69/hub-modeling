import quantities as pq
import Port
class VehicleClass:
    def __init__(self, Veh_Class, mi_kW, mi_year, className):
        self.Veh_Class = Veh_Class
        self.mi_kW = mi_kW
        self.mi_year = mi_year
        self.className = className

    def kW_Month(self):
        return (self.mi_year * (1 / self.mi_kW)).rescale('kW / month')

    def Dwell_Time(self, Port_Used):  # Capcity based on the monthly consumption of the weight vehicle class
        # h / month
        # return (self.kW_Month() * pq.hour /  ( Port_Used.Port_kW * Port_Used.Port_Efficiency)).rescale(CompoundUnit("hour / month"))
        return (self.kW_Month() * pq.hour / (Port_Used.Port_kW * Port_Used.Port_Efficiency)).rescale("hour / month")