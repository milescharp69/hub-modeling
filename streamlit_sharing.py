import streamlit as st
import pandas as pd
import numpy as np
import quantities as pq
from streamlit_echarts import st_echarts

#Global Variables
OPERATION_HOURS = pq.Quantity(24, 'hour')
NOTIONAL_HOURS = pq.Quantity(np.array([15,9]), 'hour')
sess = pq.UnitQuantity('30 minute Session', 30 * pq.min, symbol='sess')
month = pq.UnitQuantity('Month', 30 * pq.day, symbol='mon')

class Port:
    def __init__(self, Port_kW, Port_Amount, Port_Efficiency = .975):
        self.Port_kW = Port_kW
        self.Port_Amount = Port_Amount
        self.Port_Efficiency = Port_Efficiency
    
    #Port Methods
    def show(self):
        print("Port kW:", self.Port_kW)
        print("Port Amount:", self.Port_Amount)
    
    def data(self):
        return [self.Port_kW, self.Port_Amount]
class VehicleClass:
    def __init__(self, Veh_Class, mi_kW, mi_year):
        self.Veh_Class = Veh_Class
        self.mi_kW = mi_kW
        self.mi_year = mi_year
        
    def kW_Month(self):
        return (self.mi_year * (1 /self.mi_kW )).rescale('kW / month')

    def Dwell_Time(self, Port_Used): #Capcity based on the monthly consumption of the weight vehicle class         
        #h / month    
        #return (self.kW_Month() * pq.hour /  ( Port_Used.Port_kW * Port_Used.Port_Efficiency)).rescale(CompoundUnit("hour / month"))
        return (self.kW_Month() * pq.hour /  ( Port_Used.Port_kW * Port_Used.Port_Efficiency)).rescale("hour / month")
class Hub:
    def __init__(self, Hub_Type, Notional_Loading, ESVE_Ports, Vehicle_Mix, Vehicle_Classes):
        self.Hub_Type = Hub_Type
        self.Notional_Loading = Notional_Loading # [7A-10P,10P-7A]
        self.ESVE_Ports = ESVE_Ports
        self.Vehicle_Mix = np.array(Vehicle_Mix) 
        self.Vehicle_Classes = Vehicle_Classes
    
    
    #Hub Methods
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
        return int(np.sum(((self.Total_Ports() * (NOTIONAL_HOURS * self.Notional_Loading)).rescale('sess')  / (1* pq.day)).rescale('sess / mon')))
        
    
    ##########################################################################################
    """
    Max Possible amount of 30 minute Sessions per PORT per MONTH (Notional Loading applied)
    
    Month is 30 days
    """
    def Max_Sessions_Per_Port_Month(self, desiredPort = None):
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
            peak += self.ESVE_Ports[i].Port_kW * self.ESVE_Ports[i].Port_Amount * self.ESVE_Ports[i].Port_Efficiency
        return peak
    
    
    ##########################################################################################
    ################################## WORK IN PROGRESS ######################################
    ##########################################################################################
    """
    Maximum POSSIBLE number of Sessions Per Vehicle Classs (Notional Loading applied)
    Per Month
    Rounds down
    """
    
    def Max_Sessions_Per_Vehicle_Class(self, vehClass = None):
        sessionMix = self.Monthly_Svc_Sessions() * self.Vehicle_Mix
        for i in range(0,len(sessionMix)):
            sessionMix[i] = int(sessionMix[i])
            
        if vehClass != None:
            return sessionMix[vehClass]
        else:
            return sessionMix
    
    ##########################################################################################

    
    #Dwell time for each vehicle class depends on the port used 
    
    #System 1
    
    
    
    """
    Max Amount of Vehicles Service Per month by Vehicle Class
    
    Based on kW/ month  by vehicle class
    Vehicle mix 
    
    Veh Class A cannot use 1200 kW port
    
    """
    def Vehicles_Serviced_Per_Month_By_Class(self, vehClass):
        Serviced_Vehicles = 0
        #Port Usage ratio for each veh class
        if vehClass == 0 or vehClass == 1:
            if len(self.ESVE_Ports) == 1:
                portUsage = [1]
            if len(self.ESVE_Ports) == 2:
                portUsage = [.70,.30]
            if len(self.ESVE_Ports) == 3:
                portUsage = [.60,.40,0]
        if vehClass == 2:
            if len(self.ESVE_Ports) == 1:
                portUsage = [1]
            if len(self.ESVE_Ports) == 2:
                portUsage = [.70,.30]
            if len(self.ESVE_Ports) == 3:
                portUsage = [.10,.40,.50]
               
        for i in range(len(self.ESVE_Ports)):
           Serviced_Vehicles += (self.Max_Sessions_Per_Vehicle_Class()[vehClass] * portUsage[i] / (self.Vehicle_Classes[vehClass].Dwell_Time(self.ESVE_Ports[i]) * 2))
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
        print(self.Hub_Type,":\n")
        print("Max 30 minute sessions per month (Notional Loading):", self.Monthly_Svc_Sessions())
        print("- For Class 1-2 (Notional Loading):", self.Max_Sessions_Per_Vehicle_Class(0))
        print("- For Class 3-6 (Notional Loading):", self.Max_Sessions_Per_Vehicle_Class(1))
        print("- For Class 7-8 (Notional Loading):", self.Max_Sessions_Per_Vehicle_Class(2))
        print()
        print("Ports")
        for i in range(0,len(self.ESVE_Ports)):
            self.ESVE_Ports[i].show()
            print("Max 30 minute sessions per month:", self.Max_Sessions_Per_Port_Month(i))
            print()
        
        print("Number of Vehicle Serviced Per Month:", np.sum(self.Total_Vehicles_Serviced_Per_Month_By_Class()))
        print("Class 1-2 Vehicles Serviced:", self.Vehicles_Serviced_Per_Month_By_Class(0))
        print("Class 3-6 Vehicles Serviced:", self.Vehicles_Serviced_Per_Month_By_Class(1))
        print("Class 7-8 Vehicles Serviced:", self.Vehicles_Serviced_Per_Month_By_Class(2))
        

sess = pq.UnitQuantity('30 minute Session', 30 * pq.min, symbol='sess')

#Vehicles 
Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / kW') , pq.Quantity(15638, 'miles / year'))  
Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / kW') , pq.Quantity(16200, 'miles / year'))  
Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / kW') , pq.Quantity(48750, 'miles / year'))  

#Rural Hub
Hub_Name = "Rural"
Hub_Notional_Loading = np.array([0.6,0.1])
Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'),2)])
Hub_Vehicle_Mix = [0.4, 0.5, 0.1]
Vehicle_Classes = [Class_A,Class_B,Class_C]
Hub_Rural = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)
#Hub_Rural.Show()

# #Hub Page
st.title("Hub Modeling")

#Hub type selection
choice = st.selectbox(
     'Select a Hub Type',
     ('Rural', 'Urban Community', 'Urban Multimodal', 'Commercial Dominant'))

st.write('You selected:', choice)

#[{ "value": 335, "name": "Direct" }, { "value": 310, "name": "Email" },{ "value": 274, "name": "Union Ads" },{ "value": 235, "name": "Video Ads" },{ "value": 400, "name": "Search Engine" }]
if choice == 'Rural':
    pieGraphData = [{"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(0), "Name": "Class 1-2 Vehicles"},
                    {"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(1), "Name": "Class 1-2 Vehicles"},
                    {"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(2), "Name": "Class 1-2 Vehicles"}
                    ]

pieGraph = {
  "backgroundColor": "#2c343c",
  "title": {
    "text": "Vehicle Serviced",
    "left": "center",
    "top": 20,
    "textStyle": {
      "color": "#ccc"
    }
  },
  "tooltip": {
    "trigger": "item"
  },

  "series": [
    {
      "name": "Access From",
      "type": "pie",
      "radius": "55%",
      "center": ["50%", "50%"],
      "data": pieGraphData,
      "roseType": "radius",
      "label": {
        "color": "rgba(255, 255, 255, 0.3)"
      },
      "labelLine": {
        "lineStyle": {
          "color": "rgba(255, 255, 255, 0.3)"
        },
        "smooth": .3,
        "length": 10,
        "length2": 20
      },
      "itemStyle": {
        "color": "#c23531",
        "shadowBlur": 200,
        "shadowColor": "rgba(0, 0, 0, 0.5)"
      },
      "animationType": "scale",
      "animationEasing": "elasticOut",
      "animationDelay": "function (idx) {return Math.rando()* 20;}"
    }
  ]
}


st_echarts(options=pieGraph, width="100%", key=0)

