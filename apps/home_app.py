import streamlit as st
import numpy as np
import quantities as pq
from Hub import Hub
from Port import Port
from VehicleClass import VehicleClass
from streamlit_echarts import st_echarts
import copy

#Global Variables
OPERATION_HOURS = pq.Quantity(24, 'hour')
NOTIONAL_HOURS = pq.Quantity(np.array([15,9]), 'hour')
sess = pq.UnitQuantity('30 minute Session', 30 * pq.min, symbol='sess')

Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / kW') , pq.Quantity(15638, 'miles / year'), "Class 1-2")
Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / kW') , pq.Quantity(16200, 'miles / year'), 'Class 3-6')
Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / kW') , pq.Quantity(48750, 'miles / year'), 'Class 7-8')

#Preset Hubs
Hub_Name = "Rural"
Hub_Notional_Loading = np.array([0.6,0.1])
Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'),2)])
Hub_Vehicle_Mix = [0.4, 0.5, 0.1]
Vehicle_Classes = [Class_A,Class_B,Class_C]
Hub_Rural = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

Hub_Name = "Urban Community"
Hub_Notional_Loading = np.array([0.7,0.5])
Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'),2)])
Hub_Vehicle_Mix = [0.7, 0.3, 0]
Vehicle_Classes = [Class_A,Class_B,Class_C]
Hub_Urban_Community = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

Hub_Name = "Urban Multimodal"
Hub_Notional_Loading = np.array([0.7,0.5])
Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'),8), Port(pq.Quantity(300, 'kW'),2)])
Hub_Vehicle_Mix = [0.35, 0.5 , 0.15]
Vehicle_Classes = [Class_A,Class_B,Class_C]
Hub_Urban_Multimodal = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

Hub_Name = "Commercial Dominant"
Hub_Notional_Loading = np.array([0.8,0.6])
Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'),6), Port(pq.Quantity(350, 'kW'),18),Port(pq.Quantity(1000, 'kW'),16)])
Hub_Vehicle_Mix = [0.1, 0.35 , 0.55]
Vehicle_Classes = [Class_A,Class_B,Class_C]
Hub_Commercial_Dominant = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

definedHubs = [Hub_Rural, Hub_Urban_Community, Hub_Urban_Multimodal, Hub_Commercial_Dominant]
definedVehicleClasses = list(Vehicle_Classes)

def app():
    #st.markdown("Vehicle page test")
    # Bargraph
    BARGRAPH_xaxislabels = [definedHubs[i].Hub_Type for i in range(len(definedHubs))]

    # Maximum load/use
    copyDefinedHubs = copy.deepcopy(definedHubs)
    for i in range(len(copyDefinedHubs)):
        copyDefinedHubs[i].Notional_Loading = [1, 1]

    BARGRAPH_seriesdata = [{
        "name": "Class 1-2",
        "type": 'bar',
        "stack": 'Typical use',
        "emphasis": {
            "focus": 'series'
        },
        "data": [definedHubs[i].Vehicles_Serviced_Per_Month_By_Class(0) for i in range(len(definedHubs))]
    },
        {
            "name": "Class 3-6",
            "type": 'bar',
            "stack": 'Typical use',
            "emphasis": {
                "focus": 'series'
            },
            "data": [definedHubs[i].Vehicles_Serviced_Per_Month_By_Class(1) for i in range(len(definedHubs))]
        },
        {
            "name": "Class 7-8",
            "type": 'bar',
            "stack": 'Typical use',
            "emphasis": {
                "focus": 'series'
            },
            "data": [definedHubs[i].Vehicles_Serviced_Per_Month_By_Class(2) for i in range(len(definedHubs))]
        },
        {
            "name": "Class 1-2",
            "type": 'bar',
            "stack": 'max',
            "emphasis": {
                "focus": 'series'
            },
            "data": [copyDefinedHubs[i].Vehicles_Serviced_Per_Month_By_Class(0) for i in range(len(definedHubs))]
        },
        {
            "name": "Class 3-6",
            "type": 'bar',
            "stack": 'max',
            "emphasis": {
                "focus": 'series'
            },
            "data": [copyDefinedHubs[i].Vehicles_Serviced_Per_Month_By_Class(1) for i in range(len(definedHubs))]
        },
        {
            "name": "Class 7-8",
            "type": 'bar',
            "stack": 'max',
            "emphasis": {
                "focus": 'series'
            },
            "data": [copyDefinedHubs[i].Vehicles_Serviced_Per_Month_By_Class(2) for i in range(len(definedHubs))]
        }
    ]
    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'shadow'
            }
        },
        "legend": {},
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": "true"
        },
        "xAxis": [
            {
                "name": 'Hub Type',
                "type": 'category',
                "data": BARGRAPH_xaxislabels
            }
        ],
        "yAxis": [
            {
                "name": 'Vehicle Throughput',
                "type": 'value'
            }
        ],
        "series": BARGRAPH_seriesdata
    }
    st_echarts(options=option, width="100%", key=1)

