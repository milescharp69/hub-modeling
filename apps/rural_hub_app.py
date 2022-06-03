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

Hub_Name = "Rural"
Hub_Notional_Loading = np.array([0.6,0.1])
Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'),2)])
Hub_Vehicle_Mix = [0.4, 0.5, 0.1]
Vehicle_Classes = [Class_A,Class_B,Class_C]
Hub_Rural = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

# Maximum load/use
copyDefinedHubs = copy.deepcopy(Hub_Rural)
copyDefinedHubs.Notional_Loading = [1, 1]



class AppData:
    def __init__(self, peakloaddelta, classAMixdelta, classBMixdelta, classCMixdelta):
        self.peakloaddelta = peakloaddelta
        self.classAMixdelta = classAMixdelta
        self.classBMixdelta = classBMixdelta
        self.classCMixdelta = classCMixdelta
pagedata = AppData(0, 0, 0, 0)



def app():


    maininfocontainer = st.container()
    maincol1, maincol2 = maininfocontainer.columns(2)
    #submaininfocontainer = maininfocontainer.container()

    #Hub Infomations
    maincol1expander = maincol1.expander("Hub Information ", expanded=True)
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


    maincol1expander.metric("Peak kW", Hub_Rural.Peak_kW(),pagedata.peakloaddelta )
    maincol1expander.metric("Amount of ports", str(Hub_Rural.Total_Ports()))
    maincol1expander.metric("Class A Mix", str(Hub_Vehicle_Mix[0]), pagedata.classAMixdelta)
    maincol1expander.metric("Class B Mix", str(Hub_Vehicle_Mix[1]), pagedata.classBMixdelta)
    maincol1expander.metric("Class C Mix", str(Hub_Vehicle_Mix[2]), pagedata.classCMixdelta)

    maincol2expander = maincol2.expander("Sliders", expanded=True)
    maincol2expander.text("Work in progress")

    def changedeltaA(orgval):
        pagedata.classAMixdelta = round(orgval - st.session_state.class_a_slider, 2) * -1
    def changedeltaB(orgval):
        pagedata.classBMixdelta = round(orgval - st.session_state.class_b_slider, 2) * -1
    def changedeltaC(orgval):
        pagedata.classCMixdelta = round(orgval - st.session_state.class_c_slider, 2) * -1

    class_a_mix = maincol2expander.slider('Vehicle Class A Mix', 0.0, 1.0, Hub_Vehicle_Mix[0], step=0.05,
                                          key= "class_a_slider", on_change=changedeltaA, args=(Hub_Vehicle_Mix[0], )
    )

    class_b_mix = maincol2expander.slider('Vehicle Class B Mix', 0.0, 1.0, Hub_Vehicle_Mix[1], step=0.05,
                                          key= "class_b_slider", on_change=changedeltaB, args=(Hub_Vehicle_Mix[1], )
    )

    class_c_mix = maincol2expander.slider('Vehicle Class C Mix', 0.0, 1.0, Hub_Vehicle_Mix[2], step=0.05,
                                          key= "class_c_slider", on_change=changedeltaC, args=(Hub_Vehicle_Mix[2], )
    )

    if class_a_mix + class_b_mix + class_c_mix != 1:
        maincol2expander.text("Vehicle Mix should add up to 1!")


    #Figures

    figurecontainer = st.container()
    #Pie graph

    piggraphcontainer = figurecontainer.container()

    #A slider was changed
    if pagedata.classAMixdelta != 0 or  pagedata.classBMixdelta != 0 or pagedata.classCMixdelta != 0:
        piegraphcol1, piegraphcol2, piegraphcol3 = piggraphcontainer.columns(3)
        with piegraphcol1:
            pieGraphData = [{"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
                            {"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(1), "name": "Class 2-6 Vehicles"},
                            {"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(2), "name": "Class 7-8 Vehicles"}
                            ]
            pieGraphTitle = "Typical Use"
            pieGraph = {
                "backgroundColor": "#2c343c",
                "title": {
                    "text": pieGraphTitle,
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
                            "smooth": .2,
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
                        "animationDelay": "function (idx) {return Math.random()* 200;}"
                    }
                ]
            }
            st_echarts(options=pieGraph, width="100%")

        with piegraphcol2:
            pieGraphData = [{"value": copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
                            {"value": copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(1), "name": "Class 3-6 Vehicles"},
                            {"value": copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(2), "name": "Class 7-8 Vehicles"}
                            ]
            pieGraphTitle = "Maximum Use"
            pieGraph = {
                "backgroundColor": "#2c343c",
                "title": {
                    "text": pieGraphTitle,
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
                            "smooth": .2,
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
                        "animationDelay": "function (idx) {return Math.random()* 200;}"
                    }
                ]
            }
            st_echarts(options=pieGraph, width="100%")

        with piegraphcol3:
            Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / kW'), pq.Quantity(15638, 'miles / year'), "Class 1-2")
            Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / kW'), pq.Quantity(16200, 'miles / year'), 'Class 3-6')
            Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / kW'), pq.Quantity(48750, 'miles / year'), 'Class 7-8')

            Hub_Name = "Rural"
            Hub_Notional_Loading = np.array([0.6, 0.1])
            Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'), 2)])
            Vehicle_Classes = [Class_A, Class_B, Class_C]
            ruralHubCopyVehMix = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, [st.session_state.class_a_slider,
                    st.session_state.class_b_slider, st.session_state.class_c_slider], Vehicle_Classes)
            pieGraphData = [{"value": ruralHubCopyVehMix.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
                            {"value": ruralHubCopyVehMix.Vehicles_Serviced_Per_Month_By_Class(1), "name": "Class 3-6 Vehicles"},
                            {"value": ruralHubCopyVehMix.Vehicles_Serviced_Per_Month_By_Class(2), "name": "Class 7-8 Vehicles"}
                            ]
            pieGraphTitle = "Custom Use"
            pieGraph = {
                "backgroundColor": "#2c343c",
                "title": {
                    "text": pieGraphTitle,
                    "left": "center",
                    "top": 20,
                    "textStyle": {
                        "color": "#ccc"
                    }
                },
                "tooltip": {
                    "trigger": "item"
                },
                "visualMap": {
                    "show" : False,
                    "min": -215,
                    "max": 215,
                    "inRange": {
                        "colorLightness": [0, 1]
                    }
                },
                "series": [
                    {
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
                            "smooth": .2,
                            "length": 10,
                            "length2": 20
                        },
                        "itemStyle": {
                            "color": "#c23531",
                            "shadowBlur": 1000,
                            "shadowColor": "rgba(0, 0, 0, 0.5)"
                        },
                        "animationType": "scale",
                        "animationEasing": "elasticOut",
                        "animationDelay": "function (idx) {return Math.random()* 200;}"
                    }
                ]
            }
            st_echarts(options=pieGraph, width="100%")
    else:
        piegraphcol1, piegraphcol2 = piggraphcontainer.columns(2)
        with piegraphcol1:
            pieGraphData = [{"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
                            {"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(1), "name": "Class 3-6 Vehicles"},
                            {"value": Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(2), "name": "Class 7-8 Vehicles"}
                            ]
            pieGraphTitle = "Typical Use"
            pieGraph = {
                "backgroundColor": "#2c343c",
                "title": {
                    "text": pieGraphTitle,
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
                            "smooth": .2,
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
                        "animationDelay": "function (idx) {return Math.random()* 200;}"
                    }
                ]
            }
            st_echarts(options=pieGraph, width="100%")

        with piegraphcol2:
            pieGraphData = [{"value": copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(0), "name": "Class 1-2 Vehicles"},
                            {"value": copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(1), "name": "Class 2-6 Vehicles"},
                            {"value": copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(2), "name": "Class 7-8 Vehicles"}
                            ]
            pieGraphTitle = "Maximum Use"
            pieGraph = {
                "backgroundColor": "#2c343c",
                "title": {
                    "text": pieGraphTitle,
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
                            "smooth": .2,
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
                        "animationDelay": "function (idx) {return Math.random()* 200;}"
                    }
                ]
            }
            st_echarts(options=pieGraph, width="100%")

    ####################
    #Bar graph
    BARGRAPH_xaxislabels = ["Typical Use", "Max Use"]


    BARGRAPH_seriesdata = [{
        "name": "Class A",
        "type": 'bar',
        "stack": 'Ad',
        "emphasis": {
            "focus": 'series'
        },
        "data": [Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(0), copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(0)]
        },
        {
            "name": "Class B",
            "type": 'bar',
            "stack": 'Ad',
            "emphasis": {
                "focus": 'series'
            },
            "data": [Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(1), copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(1)]
        },
        {
            "name": "Class c",
            "type": 'bar',
            "stack": 'Ad',
            "emphasis": {
                "focus": 'series'
            },
            "data": [Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(2), copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(2)]
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
    bargraphexpander = figurecontainer.expander("Add text here", expanded = True)
    with bargraphexpander:
        st_echarts(options=option, width="100%")
