import streamlit as st
import pandas as pd
import numpy as np
import quantities as pq
from streamlit_echarts import st_echarts
from VehicleClass import VehicleClass
from Hub import Hub
from Port import Port
import time


#Global Variables
OPERATION_HOURS = pq.Quantity(24, 'hour')
NOTIONAL_HOURS = pq.Quantity(np.array([15,9]), 'hour')
sess = pq.UnitQuantity('30 minute Session', 30 * pq.min, symbol='sess')


#Vehicles 
Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / kW') , pq.Quantity(15638, 'miles / year'))  
Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / kW') , pq.Quantity(16200, 'miles / year'))  
Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / kW') , pq.Quantity(48750, 'miles / year'))  

#Hubs
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

# #Hub Page
st.set_page_config(layout="wide")
st.title("Hub Modeling")


#Hub type selection
with st.sidebar:
    choice = st.selectbox(
        'Select a Hub Type',
        ('Rural', 'Urban Community', 'Urban Multimodal', 'Commercial Dominant'))

    #st.write('You selected:', choice)

if choice == 'Rural':
    pieGraphData = [{"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
                    {"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(1), "name": "Class 2-6 Vehicles"},
                    {"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(2), "name": "Class 7-8 Vehicles"}
                    ]
elif choice == 'Urban Community':
    pieGraphData = [{"value": Hub_Urban_Community.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
                    {"value": Hub_Urban_Community.Vehicles_Serviced_Per_Month_By_Class(1), "name": "Class 2-6 Vehicles"},
                    {"value": Hub_Urban_Community.Vehicles_Serviced_Per_Month_By_Class(2), "name": "Class 7-8 Vehicles"}
                    ]
elif choice == 'Urban Multimodal':
    pieGraphData = [{"value": Hub_Urban_Multimodal.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
                    {"value": Hub_Urban_Multimodal.Vehicles_Serviced_Per_Month_By_Class(1), "name": "Class 2-6 Vehicles"},
                    {"value": Hub_Urban_Multimodal.Vehicles_Serviced_Per_Month_By_Class(2), "name": "Class 7-8 Vehicles"}
                    ]
else:
    pieGraphData = [{"value": Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
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

st_echarts(options=pieGraph, width="100%", key=0)


#option={"tooltip":{"trigger":"axis","axisPointer":{"type":"shadow"}},"legend":{},"grid":{"left":"3%","right":"4%","bottom":"3%","containLabel":!0},"xAxis":[{"type":"category","data":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]}],"yAxis":[{"type":"value"}],series:[{name:"Direct",type:"bar",emphasis:{focus:"series"},data:[320,332,301,334,390,330,320]},{name:"Email",type:"bar",stack:"Ad",emphasis:{focus:"series"},data:[120,132,101,134,90,230,210]},{name:"Union Ads",type:"bar",stack:"Ad",emphasis:{focus:"series"},data:[220,182,191,234,290,330,310]},{name:"Video Ads",type:"bar",stack:"Ad",emphasis:{focus:"series"},data:[150,232,201,154,190,330,410]},{name:"Search Engine",type:"bar",data:[862,1018,964,1026,1679,1600,1570],emphasis:{focus:"series"},markLine:{lineStyle:{type:"dashed"},data:[[{type:"min"},{type:"max"}]]}},{name:"Baidu",type:"bar",barWidth:5,stack:"Search Engine",emphasis:{focus:"series"},data:[620,732,701,734,1090,1130,1120]},{name:"Google",type:"bar",stack:"Search Engine",emphasis:{focus:"series"},data:[120,132,101,134,290,230,220]},{name:"Bing",type:"bar",stack:"Search Engine",emphasis:{focus:"series"},data:[60,72,71,74,190,130,110]},{name:"Others",type:"bar",stack:"Search Engine",emphasis:{focus:"series"},data:[62,82,91,84,109,110,120]}]}

BARGRAPH_xaxislabels = [definedHubs[i].Hub_Type for i in range(len(definedHubs))]
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
      "name" : 'Hub Type',
      "type": 'category',
      "data": BARGRAPH_xaxislabels
    }
  ],
  "yAxis": [
    {
      "name" : 'Vehicle Throughput',
      "type": 'value'
    }
  ],
  "series": BARGRAPH_seriesdata
}
st_echarts(options=option, width="100%", key=1)