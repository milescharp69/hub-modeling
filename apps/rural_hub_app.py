import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
import numpy as np
import altair as alt
from Hub import Hub
from Port import Port
from VehicleClass import VehicleClass
import copy



#Vehicles
# Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / (kW * hour)') , pq.Quantity(15638, 'miles / year'), "Class 1-2")
# Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / (kW * hour)') , pq.Quantity(16200, 'miles / year'), 'Class 3-6')
# Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / (kW * hour)') , pq.Quantity(48750, 'miles / year'), 'Class 7-8')
#
# Hub_Name = "Commercial Dominant"
# Hub_Notional_Loading = [0.8,0.6]
# Hub_Ports = [Port(pq.Quantity(150, 'kW')) for i in range(6)] + [Port(pq.Quantity(350, 'kW')) for i in range(18)] + \
#             [Port(pq.Quantity(1000, 'kW')) for i in range(16)]
# Hub_Vehicle_Mix = [0.1, 0.35 , 0.55]
# Vehicle_Classes = [Class_A,Class_B,Class_C]
# Hub_Commercial_Dominant = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / (kW * hour)') , pq.Quantity(15638, 'miles / year'), "Class 1-2")
Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / (kW * hour)') , pq.Quantity(16200, 'miles / year'), 'Class 3-6')
Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / (kW * hour)') , pq.Quantity(48750, 'miles / year'), 'Class 7-8')
#
Hub_Name = "Rural"
Hub_Notional_Loading = [0.6,0.1]
Hub_Ports = [Port(pq.Quantity(150, 'kW')) for i in range(2)]
Hub_Vehicle_Mix = [0.4, 0.5, 0.1]
Vehicle_Classes = [Class_A, Class_B, Class_C]
Hub_Rural = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

# Maximum load/use
#copyDefinedHubs = copy.deepcopy(Hub_Rural)
#copyDefinedHubs.Notional_Loading = [1, 1]



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
    # classmixexpander = st.sidebar.expander("Vehicle Class Mix Sliders")
    #
    # def changedeltaA(orgval):
    #     pagedata.classAMixdelta = round(orgval - st.session_state.class_a_slider, 2) * -1
    #
    # def changedeltaB(orgval):
    #     pagedata.classBMixdelta = round(orgval - st.session_state.class_b_slider, 2) * -1
    #
    # def changedeltaC(orgval):
    #     pagedata.classCMixdelta = round(orgval - st.session_state.class_c_slider, 2) * -1
    #
    # # st.sidebar.header("Vehicle Class Mix Sliders")
    # class_a_mix = classmixexpander.slider('Vehicle Class A Mix', 0.0, 1.0, Hub_Vehicle_Mix[0], step=0.05,
    #                                       key="class_a_slider", on_change=changedeltaA, args=(Hub_Vehicle_Mix[0],)
    #                                       )
    #
    # class_b_mix = classmixexpander.slider('Vehicle Class B Mix', 0.0, 1.0, Hub_Vehicle_Mix[1], step=0.05,
    #                                       key="class_b_slider", on_change=changedeltaB, args=(Hub_Vehicle_Mix[1],)
    #                                       )
    #
    # class_c_mix = classmixexpander.slider('Vehicle Class C Mix', 0.0, 1.0, Hub_Vehicle_Mix[2], step=0.05,
    #                                       key="class_c_slider", on_change=changedeltaC, args=(Hub_Vehicle_Mix[2],)
    #                                       )
    #
    # if class_a_mix + class_b_mix + class_c_mix != 1:
    #     # update Vehicle mix
    #     pagedata.copyhub.Vehicle_Mix = [class_a_mix, class_b_mix, class_c_mix]
    #     classmixexpander.text("Vehicle Mix should add up to 1!")
    #
    # pagedata.copyhub = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports,
    #                        [st.session_state.class_a_slider, st.session_state.class_b_slider,
    #                         st.session_state.class_c_slider], Vehicle_Classes)
    #
    # usage_loading_expander = st.sidebar.expander("Hub Usage Sliders")
    #
    # def changedeltausageA(orgval):
    #     pagedata.usageAdelta = round(orgval - st.session_state.usage_a_slider, 2) * -1
    #
    # def changedeltausageB(orgval):
    #     pagedata.usageBdelta = round(orgval - st.session_state.usage_b_slider, 2) * -1
    #
    # sliderUsageA = usage_loading_expander.slider('Usage 7am-10pm', 0.0, 1.0, Hub_Notional_Loading[0], step=0.05,
    #                                              key="usage_a_slider", on_change=changedeltausageA,
    #                                              args=(Hub_Notional_Loading[0],)
    #                                              )
    #
    # sliderUsageB = usage_loading_expander.slider('Usage 10pm-7am', 0.0, 1.0, Hub_Notional_Loading[1], step=0.05,
    #                                              key="usage_b_slider", on_change=changedeltausageB,
    #                                              args=(Hub_Notional_Loading[1],)
    #                                              )
    # pagedata.copyhub.Notional_Loading = [st.session_state.usage_a_slider, st.session_state.usage_b_slider]
    #
    # metric_container = st.container()
    # # metric_container.text("Hub Information")
    #
    # metric_container_info = metric_container.container()
    # metric_container_info_col1, metric_container_info_col2, metric_container_info_col3, metric_container_info_col4, metric_container_info_col5 = metric_container_info.columns(
    #     [1, 1, 1, 1, 1])
    #
    # metric_container_info_col1.metric("Usage 7am-10pm", Hub_Rural.Notional_Loading[0],
    #                                   pagedata.usageAdelta)
    # metric_container_info_col2.metric("Usage 10pm-7am", Hub_Rural.Notional_Loading[1],
    #                                   pagedata.usageBdelta)
    # metric_container_info_col3.metric("Class A Mix", str(Hub_Vehicle_Mix[0]), pagedata.classAMixdelta)
    # metric_container_info_col4.metric("Class B Mix", str(Hub_Vehicle_Mix[1]), pagedata.classBMixdelta)
    # metric_container_info_col5.metric("Class C Mix", str(Hub_Vehicle_Mix[2]), pagedata.classCMixdelta)
    #
    # # Hubinfo expander
    # hubinfocontainer = st.container()
    # hubinfocontainercol1, hubinfocontainercol2 = hubinfocontainer.columns(2)
    # maincol1expander = hubinfocontainercol1.expander("Hub Information ", expanded=True)
    # maincol1expander.markdown(
    #     """
    # <style>
    # .streamlit-expanderHeader {
    #     font-size: x-large;
    # }
    # </style>
    # """,
    #     unsafe_allow_html=True,
    # )
    # maincol1expander.markdown(
    #     "<p style='text-align: left; color: black; text-indent: 15%;'>Hub Type:       {}</p>".format(
    #         Hub_Rural.hub_id), unsafe_allow_html=True)
    # maincol1expander.markdown(
    #     "<p style='text-align: left; color: black; text-indent: 15%;'>Total Ports:        {}</p>".format(
    #         Hub_Rural.total_ports), unsafe_allow_html=True)
    # maincol1expander.markdown(
    #     "<p style='text-align: left; color: black; text-underline-offset: 20%; text-indent: 15%;'><u>Types of Ports</u></p>",
    #     unsafe_allow_html=True)
    #
    # #TODO: Fix Port Bullet port list
    #
    # # for i in range(len(Hub_Rural.esve_ports)):
    # #     maincol1expander.markdown(
    # #         "<p style='text-align: left; color: black; text-underline-offset: 20%; text-indent: 20%;'>• {}</p>".format(
    # #             Hub_Rural.esve_ports[i].datatext()),
    # #         unsafe_allow_html=True)
    #
    # # Peak load expander
    # maincol2expander = hubinfocontainercol2.expander("Peak Load", expanded=True)
    # maincol2expander.markdown("<p style='text-align: center; color: black; font-size: 25px;'>{}</p>".format(
    #     Hub_Rural.peak_load), unsafe_allow_html=True)
    # #maincol2expander.text("Work In Progress")
    #
    # # Figures
    #
    # bargraphexpander = st.expander("Vehicle Throughput")
    # ####################
    # # Bar graph
    #
    # if pagedata.usageAdelta != 0 or pagedata.usageBdelta != 0 or pagedata.classAMixdelta != 0 or pagedata.classBMixdelta != 0 or pagedata.classCMixdelta != 0:
    #     BARGRAPH_xaxislabels = ["Typical Use", "Max Use", "Custom Use"]
    #
    #     BARGRAPH_seriesdata = [{
    #         "name": "Class A",
    #         "type": 'bar',
    #         "stack": 'Ad',
    #         "emphasis": {
    #             "focus": 'series'
    #         },
    #         "data": [Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(0),
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
    #             "data": [Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(1),
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
    #             "data": [Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(2),
    #                      copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(2),
    #                      pagedata.copyhub.Vehicles_Serviced_Per_Month_By_Class(2)]
    #         }
    #
    #     ]
    #     option = {
    #         "tooltip": {
    #             "trigger": 'axis',
    #             "axisPointer": {
    #                 "type": 'shadow'
    #             }
    #         },
    #         "legend": {},
    #         "grid": {
    #             "left": '3%',
    #             "right": '4%',
    #             "bottom": '3%',
    #             "containLabel": "true"
    #         },
    #         "xAxis": [
    #             {
    #                 "name": 'Hub Type',
    #                 "type": 'category',
    #                 "data": BARGRAPH_xaxislabels
    #             }
    #         ],
    #         "yAxis": [
    #             {
    #                 "name": 'Vehicle Throughput',
    #                 "type": 'value'
    #             }
    #         ],
    #         "series": BARGRAPH_seriesdata
    #     }
    #
    #     with bargraphexpander:
    #         st_echarts(options=option, use_container_width=True)
    # else:
    #     BARGRAPH_xaxislabels = ["Typical Use", "Max Use"]
    #
    #     BARGRAPH_seriesdata = [{
    #         "name": "Class A",
    #         "type": 'bar',
    #         "stack": 'Ad',
    #         "emphasis": {
    #             "focus": 'series'
    #         },
    #         "data": [Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(0),
    #                  copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(0)]
    #     },
    #         {
    #             "name": "Class B",
    #             "type": 'bar',
    #             "stack": 'Ad',
    #             "emphasis": {
    #                 "focus": 'series'
    #             },
    #             "data": [Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(1),
    #                      copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(1)]
    #         },
    #         {
    #             "name": "Class c",
    #             "type": 'bar',
    #             "stack": 'Ad',
    #             "emphasis": {
    #                 "focus": 'series'
    #             },
    #             "data": [Hub_Rural.Vehicles_Serviced_Per_Month_By_Class(2),
    #                      copyDefinedHubs.Vehicles_Serviced_Per_Month_By_Class(2)]
    #         }
    #
    #     ]
    #     option = {
    #         "tooltip": {
    #             "trigger": 'axis',
    #             "axisPointer": {
    #                 "type": 'shadow'
    #             }
    #         },
    #         "legend": {},
    #         "grid": {
    #             "left": '3%',
    #             "right": '4%',
    #             "bottom": '3%',
    #             "containLabel": "true"
    #         },
    #         "xAxis": [
    #             {
    #                 "name": 'Hub Type',
    #                 "type": 'category',
    #                 "data": BARGRAPH_xaxislabels
    #             }
    #         ],
    #         "yAxis": [
    #             {
    #                 "name": 'Vehicle Throughput',
    #                 "type": 'value'
    #             }
    #         ],
    #         "series": BARGRAPH_seriesdata
    #     }
    #     with bargraphexpander:
    #         st_echarts(options=option, use_container_width=True)
    #
    #
    # # st.text(Hub_Rural.Hub_Type)
    # # st.text(Hub_Rural.Vehicle_Classes[0].monthly_consumption() * Hub_Rural.Vehicle_Classes[0].Dwell_Time())
    #
    # test = st.empty()

    # chart = (
    # alt.Chart(Hub_Rural.simulate_hub_data('1/25/2022')).mark_line().transform_window(
    #     # Sort the data chronologically
    #     sort=[{'field': 'date'}],
    #     # Include all previous records before the current record and none after
    #     # (This is the default value so you could skip it and it would still work.)
    #     frame=[None, 0],
    #     # What to add up as you go
    #     Energy='sum(Consumption)'
    # ).encode(
    #     alt.X('yearmonthdatehoursminutes(date):Q',
    #           title='date'
    #           ),
    #     # Plot the calculated field created by the transformation
    #     y='Energy:Q'
    # ).interactive()
    # )
    # test.altair_chart(chart.interactive(), use_container_width=True)


    # alt.Chart(data.reset_index()).mark_line().encode(
    #     x='index:T',
    #     y='value:Q'
    # )

    #Consumption Chart
    st.write(Hub_Rural.hub_id)
    consumption_chart_container = st.empty()
    Data = Hub_Rural.simulate_hub_data('12/31/2022').reset_index()
    st.write(Data)
    chart = (alt.Chart(Data).mark_bar().encode(
        alt.Y('yearmonth(Index):O',
              title='Date',
              axis=alt.Axis(labelAngle=325)
              ),
        alt.X('sum(Consumption)',
              title="Consumption MWh",
              stack='zero'),
        color='Vehicle'
    ))
    chart.height = 200
    text = alt.Chart(Data).mark_text(dx=-30, color='black', align='left').encode(
        alt.Y('yearmonth(Index):O',),
        alt.X('sum(Consumption)', stack='zero'),
        detail='Vehicle:N',
        text=alt.Text('sum(Consumption):Q', format='.1f')
    )

    consumption_chart_container.altair_chart(chart + text, use_container_width=True)

    chart_sessions_con = st.empty()
    chart_sessions = (alt.Chart(Data).mark_bar().encode(
        alt.Y('yearmonth(Index):O',
              title='Date',
              axis=alt.Axis(labelAngle=325)
              ),
        alt.X('sum(Sessions)',
              title="Sessions",
              stack='zero'),
        color='Vehicle'
    ))
    chart_sessions.height = 200
    text_sessions = alt.Chart(Data).mark_text(dx= -20, align= 'center', color='black').encode(
        alt.Y('yearmonth(Index):O',),
        alt.X('sum(Sessions)', stack='zero'),
        detail='Vehicle:N',
        text=alt.Text('sum(Sessions):Q', format='.1f')
    )
    chart_sessions_con.altair_chart(chart_sessions + text_sessions, use_container_width=True)



    # chart = (alt.Chart(Data).mark_bar().encode(
    #     alt.X('yearmonth(Index):O',
    #           title='Date',
    #           axis=alt.Axis(labelAngle=325)
    #           ),
    #     alt.Y('sum(Consumption)',
    #           title="Consumption MWh"
    #           )
    #     ,
    #     color = 'Vehicle'
    # ))
    #
    # text = alt.Chart(Data).mark_text(dy=-5, color='white', align='center').encode(
    #     x='yearmonth(Index):O',
    #     y='sum(Consumption)',
    #     detail='Vehicle:N',
    #     text=alt.Text('sum(Consumption):Q', format='.1f')
    # )
    #
    # consumption_chart_container.altair_chart(chart + text, use_container_width=True)

    # Peak kW Chart

    # Sessions Chart
        #Show Sessions per Vehicle Class
    # Cost/revenuse/Profit