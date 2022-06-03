import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
import numpy as np
from Hub import Hub
from Port import Port
from VehicleClass import VehicleClass

#Vehicles
Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / kW') , pq.Quantity(15638, 'miles / year'), "Class 1-2")
Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / kW') , pq.Quantity(16200, 'miles / year'), 'Class 3-6')
Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / kW') , pq.Quantity(48750, 'miles / year'), 'Class 7-8')

Hub_Name = "Commercial Dominant"
Hub_Notional_Loading = np.array([0.8,0.6])
Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'),6), Port(pq.Quantity(350, 'kW'),18),Port(pq.Quantity(1000, 'kW'),16)])
Hub_Vehicle_Mix = [0.1, 0.35 , 0.55]
Vehicle_Classes = [Class_A,Class_B,Class_C]
Hub_Commercial_Dominant = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

pieGraphData = [
    {"value": Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
    {"value": Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(1), "name": "Class 2-6 Vehicles"},
    {"value": Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(2), "name": "Class 7-8 Vehicles"}
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


def app():
    st_echarts(options=pieGraph, width="100%", key=3)