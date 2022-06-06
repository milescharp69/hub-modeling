import Port
import VehicleClass
import numpy as np
import quantities as pq
#Global Variables
OPERATION_HOURS = pq.Quantity(24, 'hour')
NOTIONAL_HOURS = pq.Quantity(np.array([15,9]), 'hour')
sess = pq.UnitQuantity('30 minute Session', 30 * pq.min, symbol='sess')

class Hub:
    def __init__(self, Hub_Type, Notional_Loading, ESVE_Ports, Vehicle_Mix, Vehicle_Classes):
        self.Hub_Type = Hub_Type
        self.Notional_Loading = Notional_Loading  # [7A-10P,10P-7A]
        self.ESVE_Ports = ESVE_Ports
        self.Vehicle_Mix = np.array(Vehicle_Mix)
        self.Vehicle_Classes = Vehicle_Classes

    # Hub Methods
    def set_mix(self, a, b, c):
        self.Vehicle_Mix = [a,b,c]


    def Total_Ports(self):
        totalPorts = 0
        for i in range(0, len(self.ESVE_Ports)):
            totalPorts += self.ESVE_Ports[i].Port_Amount

        return totalPorts

    ##########################################################################################
    """
    Max Possible amount of 30 minute Sessions per Month (Notional Loading applied)

    This function doesn't account for the fact that Veh class 1-2 cannot use a 1.2MWPort and Veh Clas 7-8 will most likely not use 
    a 150 kW port
    """

    def Monthly_Svc_Sessions(self):
        return int(np.sum(
            ((self.Total_Ports() * (NOTIONAL_HOURS * self.Notional_Loading)).rescale('sess') / (1 * pq.day)).rescale(
                'sess / month')))

    ##########################################################################################
    """
    Max Possible amount of 30 minute Sessions per PORT per MONTH (Notional Loading applied)

    Month is 30 days
    """

    def Max_Sessions_Per_Port_Month(self, desiredPort=None):
        portsAval = []
        for i in range(0, len(self.ESVE_Ports)):
            portsAval.append(self.ESVE_Ports[i].Port_Amount)
        portRatio = np.array(portsAval) / self.Total_Ports()
        sessionPorts = self.Monthly_Svc_Sessions() * portRatio
        if desiredPort != None:
            return sessionPorts[desiredPort]
        return sessionPorts

    ##########################################################################################
    """
    Max Possible amount of 30 minute Sessions per MONTH (Notional Loading applied)

    Month is 30 days
    """

    def Max_30Min_Sessions_Month(self):
        return 30 * 2 * OPERATION_HOURS * self.Total_Ports()

    ##########################################################################################

    def Peak_kW(self):  # Ask about this applied efficency
        peak = 0
        for i in range(0, len(self.ESVE_Ports)):
            peak += ((self.ESVE_Ports[i].Port_kW).rescale('kW')).magnitude * self.ESVE_Ports[i].Port_Amount * self.ESVE_Ports[i].Port_Efficiency
        return pq.Quantity(peak, 'kW')

    ##########################################################################################
    ################################## WORK IN PROGRESS ######################################
    ##########################################################################################
    """
    Maximum POSSIBLE number of Sessions Per Vehicle Classs (Notional Loading applied)
    Per Month
    Rounds down
    """

    def Max_Sessions_Per_Vehicle_Class(self, vehClass=None):
        sessionMix = self.Monthly_Svc_Sessions() * self.Vehicle_Mix
        for i in range(0, len(sessionMix)):
            sessionMix[i] = int(sessionMix[i])

        if vehClass != None:
            return sessionMix[vehClass]
        else:
            return sessionMix

    ##########################################################################################

    # Dwell time for each vehicle class depends on the port used

    # System 1

    """
    Max Amount of Vehicles Service Per month by Vehicle Class

    Based on kW/ month  by vehicle class
    Vehicle mix 

    Veh Class A cannot use 1200 kW port

    """

    def Vehicles_Serviced_Per_Month_By_Class(self, vehClass):
        Serviced_Vehicles = 0
        # Port Usage ratio for each veh class
        if vehClass == 0 or vehClass == 1:
            if len(self.ESVE_Ports) == 1:
                portUsage = [1]
            if len(self.ESVE_Ports) == 2:
                portUsage = [.70, .30]
            if len(self.ESVE_Ports) == 3:
                portUsage = [.60, .40, 0]
        if vehClass == 2:
            if len(self.ESVE_Ports) == 1:
                portUsage = [1]
            if len(self.ESVE_Ports) == 2:
                portUsage = [.70, .30]
            if len(self.ESVE_Ports) == 3:
                portUsage = [.10, .40, .50]

        for i in range(len(self.ESVE_Ports)):
            Serviced_Vehicles += (self.Max_Sessions_Per_Vehicle_Class()[vehClass] * portUsage[i] / (
                        self.Vehicle_Classes[vehClass].Dwell_Time(self.ESVE_Ports[i]) * 2))
        return int(Serviced_Vehicles)

    #     """
    #     Total amount of vehicles Serviced per Month
    #     """
    def Total_Vehicles_Serviced_Per_Month_By_Class(self):
        total = []
        for i in range(len(self.Vehicle_Classes)):
            total.append(self.Vehicles_Serviced_Per_Month_By_Class(i))
        return total

    def Show(self):
        return
        (
        """
        Hub_Type = {} \n
        Notional_Loading =  {} \n
        ESVE_Ports = {} \n
        Vehicle_Mix = {} \n
        Vehicle_Classes = {} \n0
        """.format(self.Hub_Type, self.Notional_Loading, self.ESVE_Ports, self.Vehicle_Mix, self.Vehicle_Classes ))
        # return ("""
        # Max 30 minute sessions per month (Notional Loading {} \n
        # - For Class 1-2 (Notional Loading): {} \n
        # - For Class 3-6 (Notional Loading): {} \n
        # - For Class 7-8 (Notional Loading): {} \n
        # Number of Vehicle Serviced Per Month {} \n
        # - {} \n
        # - {} \n
        # - {}
        # """.format(self.Monthly_Svc_Sessions(), self.Max_Sessions_Per_Vehicle_Class(0), self.Max_Sessions_Per_Vehicle_Class(1), self.Max_Sessions_Per_Vehicle_Class(2),
        #            np.sum(self.Total_Vehicles_Serviced_Per_Month_By_Class()),
        #            self.Vehicles_Serviced_Per_Month_By_Class(0),
        #            self.Vehicles_Serviced_Per_Month_By_Class(1),
        #            self.Vehicles_Serviced_Per_Month_By_Class(2)
        #            ))