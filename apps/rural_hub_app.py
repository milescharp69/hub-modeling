import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
import numpy as np
import altair as alt
from Hub import Hub
from Port import Port

from st_aggrid import AgGrid

from VehicleClass import car


Hub_Name = "Rural"
Hub_Notional_Loading = [0.6,0.1]
Hub_Ports = [Port(pq.Quantity(150, 'kW')) for i in range(2)]
Hub_Vehicle_Mix = [0.4, 0.5, 0.1]
hub = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix)


def app():


    # Sidebar code
    classmix_expander = st.sidebar.expander("Vehicle Class Mix Sliders")

    # st.sidebar.header("Vehicle Class Mix Sliders")
    class_a_mix = classmix_expander.slider('Vehicle Class A Mix', 0.0, 1.0, Hub_Vehicle_Mix[0], step=0.05,
                                          key="class_a_slider")
    class_b_mix = classmix_expander.slider('Vehicle Class B Mix', 0.0, 1.0, Hub_Vehicle_Mix[1], step=0.05,
                                          key="class_b_slider")
    class_c_mix = classmix_expander.slider('Vehicle Class C Mix', 0.0, 1.0, Hub_Vehicle_Mix[2], step=0.05,
                                          key="class_c_slider")

    if class_a_mix + class_b_mix + class_c_mix != 1:
        # update Vehicle mix
        classmix_expander.text("Vehicle Mix should add up to 1!")


    usage_loading_expander = st.sidebar.expander("Hub Usage Sliders")


    sliderUsageA = usage_loading_expander.slider('Usage 7am-10pm', 0.0, 1.0, Hub_Notional_Loading[0], step=0.05,
                                                 key="usage_a_slider")

    sliderUsageB = usage_loading_expander.slider('Usage 10pm-7am', 0.0, 1.0, Hub_Notional_Loading[1], step=0.05,
                                                 key="usage_b_slider")

    metric_container = st.container()

    metric_container_info = metric_container.container()
    metric_container_info_col1, metric_container_info_col2, metric_container_info_col3, metric_container_info_col4, metric_container_info_col5 = metric_container_info.columns(
        [1, 1, 1, 1, 1])

    metric_container_info_col1.metric("Usage 7am-10pm", hub.vehicle_mix[0],
                                      round(abs(hub.usage_factor[0] - st.session_state.usage_a_slider), 2))
    metric_container_info_col2.metric("Usage 10pm-7am", hub.vehicle_mix[1],
                                      round(abs(hub.usage_factor[0] - st.session_state.usage_b_slider), 2))

    metric_container_info_col3.metric("Class A Mix", str(Hub_Vehicle_Mix[0]),
                                      round(abs(hub.vehicle_mix[0] - st.session_state.class_a_slider), 2))
    metric_container_info_col4.metric("Class B Mix", str(Hub_Vehicle_Mix[1]),
                                      round(abs(hub.vehicle_mix[0] - st.session_state.class_b_slider), 2))
    metric_container_info_col5.metric("Class C Mix", str(Hub_Vehicle_Mix[2]),
                                      round(abs(hub.vehicle_mix[0] - st.session_state.class_c_slider), 2))

    hub_copy = Hub(Hub_Name, [st.session_state.usage_a_slider, st.session_state.usage_a_slider],
                   Hub_Ports, [st.session_state.class_a_slider, st.session_state.class_b_slider,
                               st.session_state.class_c_slider])

    #Check is hub was changed
    if hub.usage_factor != hub_copy.usage_factor or hub.vehicle_mix != hub_copy.vehicle_mix:
        hub_changed = True
    elif hub.usage_factor == hub_copy.usage_factor or hub.vehicle_mix == hub_copy.vehicle_mix:
        hub_changed = False



    # Hubinfo expander
    hubinfocontainer = st.container()
    hubinfocontainercol1, hubinfocontainercol2 = hubinfocontainer.columns(2)
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

    maincol1expander.markdown(
        "<p style='text-align: left; color: black; text-indent: 15%;'>Hub Type:       {}</p>".format(
            hub.hub_id), unsafe_allow_html=True)
    maincol1expander.markdown(
        "<p style='text-align: left; color: black; text-indent: 15%;'>Total Ports:        {}</p>".format(
            hub.total_ports), unsafe_allow_html=True)
    maincol1expander.markdown(
        "<p style='text-align: left; color: black; text-underline-offset: 20%; text-indent: 15%;'><u>Types of Ports</u></p>",
        unsafe_allow_html=True)

    for i in hub.port_types.keys():
        maincol1expander.markdown(
            "<p style='text-align: left; color: black; text-underline-offset: 20%; text-indent: 20%;'>• {}</p>".format(
                str(int(i))+"kW x "+str(hub.port_types[i])),
            unsafe_allow_html=True)

    # Peak load expander
    # maincol2expander = hubinfocontainercol2.expander("Peak Load", expanded=True)
    # maincol2expander.markdown("<p style='text-align: center; color: black; font-size: 25px;'>{}</p>".format(
    #     Hub_Rural.peak_load), unsafe_allow_html=True)
    #maincol2expander.text("Work In Progress")


    # Figures

    bargraphexpander = st.expander("Vehicle Throughput")


    ####################
    # Bar graph
    # hub_max = Hub(Hub_Name, [0,0], Hub_Ports, Hub_Vehicle_Mix)
    #
    # if hub_changed:
    #     BARGRAPH_xaxislabels = ["Typical Use", "Max Use", "Custom Use"]
    #     BARGRAPH_seriesdata = [{
    #         "name": "Class A",
    #         "type": 'bar',
    #         "stack": 'Ad',
    #         "emphasis": {
    #             "focus": 'series'
    #         },
    #         "data": [hub.Vehicles_Serviced_Per_Month_By_Class(0),
    #                  copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(0),
    #                  pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(0)]
    #     },
    #         {
    #             "name": "Class B",
    #             "type": 'bar',
    #             "stack": 'Ad',
    #             "emphasis": {
    #                 "focus": 'series'
    #             },
    #             "data": [hub.Vehicles_Serviced_Per_Month_By_Class(1),
    #                      copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(1),
    #                      pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(1)]
    #         },
    #         {
    #             "name": "Class c",
    #             "type": 'bar',
    #             "stack": 'Ad',
    #             "emphasis": {
    #                 "focus": 'series'
    #             },
    #             "data": [hub.Vehicles_Serviced_Per_Month_By_Class(2),
    #                      copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(2),
    #                      pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(2)]
    #         }
    #
    #     ]
    # else:
    #     BARGRAPH_xaxislabels = ["Typical Use", "Max Use"]
    #     BARGRAPH_seriesdata = [{
    #         "name": "Class A",
    #         "type": 'bar',
    #         "stack": 'Ad',
    #         "emphasis": {
    #             "focus": 'series'
    #         },
    #         "data": [hub.Vehicles_Serviced_Per_Month_By_Class(0),
    #                  copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(0),
    #                  pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(0)]
    #     },
    #         {
    #             "name": "Class B",
    #             "type": 'bar',
    #             "stack": 'Ad',
    #             "emphasis": {
    #                 "focus": 'series'
    #             },
    #             "data": [hub.Vehicles_Serviced_Per_Month_By_Class(1),
    #                      copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(1),
    #                      pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(1)]
    #         },
    #         {
    #             "name": "Class c",
    #             "type": 'bar',
    #             "stack": 'Ad',
    #             "emphasis": {
    #                 "focus": 'series'
    #             },
    #             "data": [hub.Vehicles_Serviced_Per_Month_By_Class(2),
    #                      copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(2),
    #                      pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(2)]
    #         }
    #
    #     ]
    #
    # option = {
    #     "tooltip": {
    #         "trigger": 'axis',
    #         "axisPointer": {
    #             "type": 'shadow'
    #         }
    #     },
    #     "legend": {},
    #     "grid": {
    #         "left": '3%',
    #         "right": '4%',
    #         "bottom": '3%',
    #         "containLabel": "true"
    #     },
    #     "xAxis": [
    #         {
    #             "name": 'Hub Type',
    #             "type": 'category',
    #             "data": BARGRAPH_xaxislabels
    #         }
    #     ],
    #     "yAxis": [
    #         {
    #             "name": 'Vehicle Throughput',
    #             "type": 'value'
    #         }
    #     ],
    #     "series": BARGRAPH_seriesdata
    # }
    #
    # with bargraphexpander:
    #     st_echarts(options=option, use_container_width=True)
    df = hub.graphic_sim('1/30/2022')
    df_styled = df.style.applymap(lambda x: "background-color: red" if x is False else "background-color: white")
    schedule_expander = st.expander("Hub Schedule")
    schedule_expander.dataframe(df_styled)
    AgGrid(df)
