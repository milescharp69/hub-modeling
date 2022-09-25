import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
import numpy as np
from Hub import Hub
from Port import Port
from VehicleClass import VehicleClass
import copy

#Vehicles
Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / (kW * hour)') , pq.Quantity(15638, 'miles / year'), "Class 1-2")
Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / (kW * hour)') , pq.Quantity(16200, 'miles / year'), 'Class 3-6')
Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / (kW * hour)') , pq.Quantity(48750, 'miles / year'), 'Class 7-8')

Hub_Name = "Rural"
Hub_Notional_Loading = [0.6,0.1]
#np.array([Port(pq.Quantity(150, 'kW'),6), Port(pq.Quantity(350, 'kW'),18),Port(pq.Quantity(1000, 'kW'),16)])
Hub_Ports = [Port(pq.Quantity(150, 'kW')) for i in range(2)]
Hub_Vehicle_Mix = [0.4, 0.5, 0.1]

Vehicle_Classes = [Class_A,Class_B,Class_C]
Hub_Commercial_Dominant = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)


# Maximum load/use
copyDefinedHubs = copy.deepcopy(Hub_Commercial_Dominant)
copyDefinedHubs.Notional_Loading = [1, 1]

class AppData:
    def __init__(self, peakloaddelta, classAMixdelta, classBMixdelta, classCMixdelta, usageAdelta, usageBdelta):
        self.peakloaddelta = peakloaddelta
        self.classAMixdelta = classAMixdelta
        self.classBMixdelta = classBMixdelta
        self.classCMixdelta = classCMixdelta
        self.usageAdelta = usageAdelta
        self.usageBdelta = usageBdelta
        self.copyhub = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)
pagedata = AppData(0, 0, 0, 0, 0, 0)


def app():
    st.write(Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(0))
    classmixexpander = st.sidebar.expander("Vehicle Class Mix Sliders")

    def changedelta_a(orgval):
        pagedata.classAMixdelta = round(orgval - st.session_state.class_a_slider, 2) * -1

    def changedeltaB(orgval):
        pagedata.classBMixdelta = round(orgval - st.session_state.class_b_slider, 2) * -1

    def changedeltaC(orgval):
        pagedata.classCMixdelta = round(orgval - st.session_state.class_c_slider, 2) * -1

    class_a_mix = classmixexpander.slider('Vehicle Class A Mix', 0.0, 1.0, Hub_Vehicle_Mix[0], step=0.05,
                                          key="class_a_slider", on_change=changedelta_a, args=(Hub_Vehicle_Mix[0],)
                                          )

    class_b_mix = classmixexpander.slider('Vehicle Class B Mix', 0.0, 1.0, Hub_Vehicle_Mix[1], step=0.05,
                                          key="class_b_slider", on_change=changedeltaB, args=(Hub_Vehicle_Mix[1], )
    )

    class_c_mix = classmixexpander.slider('Vehicle Class C Mix', 0.0, 1.0, Hub_Vehicle_Mix[2], step=0.05,
                                          key="class_c_slider", on_change=changedeltaC, args=(Hub_Vehicle_Mix[2], )
    )

    if class_a_mix + class_b_mix + class_c_mix != 1:
        # Update Vehicle mix
        pagedata.copyhub.vehicle_mix = [class_a_mix, class_b_mix, class_c_mix]
        classmixexpander.text("Vehicle Mix should add up to 1!")

    pagedata.copyhub = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, [st.session_state.class_a_slider, st.session_state.class_b_slider, st.session_state.class_c_slider], Vehicle_Classes)

    usage_loading_expander = st.sidebar.expander("Hub Usage Sliders")

    def changedeltausageA(orgval):
        pagedata.usageAdelta = round(orgval - st.session_state.usage_a_slider, 2) * -1

    def changedeltausageB(orgval):
        pagedata.usageBdelta = round(orgval - st.session_state.usage_b_slider, 2) * -1

    sliderUsageA = usage_loading_expander.slider('Usage 7am-10pm', 0.0, 1.0, Hub_Notional_Loading[0], step=0.05,
                                          key= "usage_a_slider", on_change=changedeltausageA, args=(Hub_Notional_Loading[0], )
        )

    sliderUsageB = usage_loading_expander.slider('Usage 10pm-7am', 0.0, 1.0, Hub_Notional_Loading[1], step=0.05,
                                          key= "usage_b_slider", on_change=changedeltausageB, args=(Hub_Notional_Loading[1], )
        )
    pagedata.copyhub.usage_factor = [st.session_state.usage_a_slider, st.session_state.usage_b_slider]

    metric_container = st.container()

    metric_container_info = metric_container.container()
    metric_container_info_col1, metric_container_info_col2, metric_container_info_col3, metric_container_info_col4, \
        metric_container_info_col5 = metric_container_info.columns([1, 1, 1, 1, 1])

    metric_container_info_col1.metric("Usage 7am-10pm", Hub_Commercial_Dominant.usage_factor[0], pagedata.usageAdelta)
    metric_container_info_col2.metric("Usage 10pm-7am", Hub_Commercial_Dominant.usage_factor[1], pagedata.usageBdelta)
    metric_container_info_col3.metric("Class A Mix", str(Hub_Vehicle_Mix[0]), pagedata.classAMixdelta)
    metric_container_info_col4.metric("Class B Mix", str(Hub_Vehicle_Mix[1]), pagedata.classBMixdelta)
    metric_container_info_col5.metric("Class C Mix", str(Hub_Vehicle_Mix[2]), pagedata.classCMixdelta)


    #Hubinfo expander
    hubinfocontainer = st.container()
    hubinfocontainercol1 , hubinfocontainercol2 = hubinfocontainer.columns(2)
    maincol1expander = hubinfocontainercol1.expander("Hub Information ", expanded=True)
    maincol1expander.markdown(
        """
    <style>
    .streamlit-expanderHeader {
        font-size: x-large;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    maincol1expander.markdown("<p style='text-align: left; color: black; text-indent: 15%;'>Hub Type:       {}</p>".format(Hub_Commercial_Dominant.hub_id), unsafe_allow_html=True)
    maincol1expander.markdown("<p style='text-align: left; color: black; text-indent: 15%;'>Total Ports:        {}</p>".format(Hub_Commercial_Dominant.total_ports()), unsafe_allow_html=True)
    # maincol1expander.markdown("<p style='text-align: left; color: black; text-underline-offset: 20%; text-indent: 15%;'><u>Types of Ports</u></p>", unsafe_allow_html=True)
    # for i in range(len(Hub_Commercial_Dominant.hub_ports)):
    #     maincol1expander.markdown(
    #         "<p style='text-align: left; color: black; text-underline-offset: 20%; text-indent: 20%;'>• {}</p>".format(Hub_Commercial_Dominant.hub_ports[i].datatext()),
    #         unsafe_allow_html=True)


    #Peak load expander
    maincol2expander = hubinfocontainercol2.expander("Peak Load", expanded=True)
    maincol2expander.markdown("<p style='text-align: center; color: black; font-size: 25px;'>{}</p>".format(Hub_Commercial_Dominant.Peak_kW()), unsafe_allow_html=True)
    maincol2expander.text("Work In Progress")

    #Figures

    bargraphexpander = st.expander("Vehicle Throughput per Hub use")
    ####################
    #Bar graph

    if pagedata.usageAdelta != 0 or pagedata.usageBdelta != 0 or pagedata.classAMixdelta != 0 or pagedata.classBMixdelta != 0 or pagedata.classCMixdelta != 0:
        BARGRAPH_xaxislabels = ["Typical Use", "Max Use", "Custom Use"]

        BARGRAPH_seriesdata = [{
            "name": "Class A",
            "type": 'bar',
            "stack": 'Ad',
            "emphasis": {
                "focus": 'series'
            },
            "data": [Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(0),
                     copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(0),
                     pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(0)]
        },
            {
                "name": "Class B",
                "type": 'bar',
                "stack": 'Ad',
                "emphasis": {
                    "focus": 'series'
                },
                "data": [Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(1),
                         copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(1),
                         pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(1)]
            },
            {
                "name": "Class c",
                "type": 'bar',
                "stack": 'Ad',
                "emphasis": {
                    "focus": 'series'
                },
                "data": [Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(2),
                         copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(2),
                         pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(2)]
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
        with bargraphexpander:
            st_echarts(options=option, width="100%")
    else:
        BARGRAPH_xaxislabels = ["Typical Use", "Max Use"]

        BARGRAPH_seriesdata = [{
            "name": "Class A",
            "type": 'bar',
            "stack": 'Ad',
            "emphasis": {
                "focus": 'series'
            },
            "data": [Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(0),
                     copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(0)]
        },
            {
                "name": "Class B",
                "type": 'bar',
                "stack": 'Ad',
                "emphasis": {
                    "focus": 'series'
                },
                "data": [Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(1),
                         copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(1)]
            },
            {
                "name": "Class c",
                "type": 'bar',
                "stack": 'Ad',
                "emphasis": {
                    "focus": 'series'
                },
                "data": [Hub_Commercial_Dominant.Vehicles_Serviced_Per_Month_By_Class(2),
                         copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(2)]
            }

        ]
        bargraphexpander.write(BARGRAPH_seriesdata)
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
        with bargraphexpander:
            st_echarts(options=option, width="100%")





