import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
import numpy as np
from Hub import Hub
from Port import Port
from VehicleClass import VehicleClass
import copy

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

# Maximum load/use
copyDefinedHubs = copy.deepcopy(Hub_Commercial_Dominant)
copyDefinedHubs.Notional_Loading = [1, 1]

class AppData:
    def __init__(self, peakloaddelta, classAMixdelta, classBMixdelta, classCMixdelta):
        self.peakloaddelta = peakloaddelta
        self.classAMixdelta = classAMixdelta
        self.classBMixdelta = classBMixdelta
        self.classCMixdelta = classCMixdelta
pagedata = AppData(0, 0, 0, 0)


def app():
    check_notional_loading = st.sidebar.checkbox("Notional Loading")
    # def change_notional_loading_a():
    #
    # def change_notional_loading_b():
    #
    # if check_notional_loading:
    #     notional_loading_a = st.sidebar.slider('Vehicle Class A Mix', 0.0, 1.0, Hub_Vehicle_Mix[0], step=0.05,
    #                                     key="class_a_slider", on_change=change_notional_loading_a, args=(Hub_Vehicle_Mix[0],)
    #                                     )
    #     notional_loading_b = st.sidebar.slider('Vehicle Class A Mix', 0.0, 1.0, Hub_Vehicle_Mix[0], step=0.05,
    #                                           key= "class_a_slider", on_change=changedeltaA, args=(Hub_Vehicle_Mix[0], )
    #     )
    check_vehicle_mix = st.sidebar.checkbox("Vehicle Mix")

    # if check_vehicle_mix:
    #     def changedeltaA(orgval):
    #         pagedata.classAMixdelta = round(orgval - st.session_state.class_a_slider, 2) * -1
    #     def changedeltaB(orgval):
    #         pagedata.classBMixdelta = round(orgval - st.session_state.class_b_slider, 2) * -1
    #     def changedeltaC(orgval):
    #         pagedata.classCMixdelta = round(orgval - st.session_state.class_c_slider, 2) * -1
    #
    #     class_a_mix = st.sidebar.slider('Vehicle Class A Mix', 0.0, 1.0, Hub_Vehicle_Mix[0], step=0.05,
    #                                           key= "class_a_slider", on_change=changedeltaA, args=(Hub_Vehicle_Mix[0], )
    #     )
    #
    #     class_b_mix = st.sidebar.slider('Vehicle Class B Mix', 0.0, 1.0, Hub_Vehicle_Mix[1], step=0.05,
    #                                           key= "class_b_slider", on_change=changedeltaB, args=(Hub_Vehicle_Mix[1], )
    #     )
    #
    #     class_c_mix = st.sidebar.slider('Vehicle Class C Mix', 0.0, 1.0, Hub_Vehicle_Mix[2], step=0.05,
    #                                           key= "class_c_slider", on_change=changedeltaC, args=(Hub_Vehicle_Mix[2], )
    #     )


    metric_container = st.container()
    metric_container.text("Hub Information")

    metric_container_info = metric_container.container()
    metric_container_info_col1, metric_container_info_col2, metric_container_info_col3, metric_container_info_col4, metric_container_info_col5, metric_container_info_col6 = metric_container_info.columns([1,1,1,1,1,1])
    metric_container_info_col2.metric("Peak kW", Hub_Commercial_Dominant.Peak_kW())

    metric_container_info_col3.metric("Class A Mix", str(Hub_Vehicle_Mix[0]), pagedata.classAMixdelta)
    metric_container_info_col4.metric("Class B Mix", str(Hub_Vehicle_Mix[1]), pagedata.classBMixdelta)
    metric_container_info_col5.metric("Class C Mix", str(Hub_Vehicle_Mix[2]), pagedata.classCMixdelta)




    #Port infomation
    metric_container_ports = metric_container.container()
    metric_container_ports.markdown("<h1 style='text-align: center; color: black;'>Port Breakdown</h1>", unsafe_allow_html=True)

    metric_container_ports1, metric_container_ports2, metric_container_ports3, metric_container_ports4, metric_container_ports5 = metric_container_ports.columns(5)
    metric_container_ports3.metric("Amount of ports", str(Hub_Commercial_Dominant.Total_Ports()))

    metric_container_subports = metric_container.container()

    #port breakdown
    metric_container_subports1, metric_container_subports2, metric_container_subports3, metric_container_subports4, metric_container_subports5 = metric_container_subports.columns(5)
    metric_container_subports2.metric("Class A Mix", str(Hub_Vehicle_Mix[0]), pagedata.classAMixdelta)
    metric_container_subports3.metric("Class A Mix", str(Hub_Vehicle_Mix[0]), pagedata.classAMixdelta)
    metric_container_subports4.metric("Class A Mix", str(Hub_Vehicle_Mix[0]), pagedata.classAMixdelta)