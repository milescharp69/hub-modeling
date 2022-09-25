import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
import numpy as np
import altair as alt
from Hub import Hub
from Port import Port
from VehicleClass import car

Hub_Name = "Rural"
Hub_Notional_Loading = [0.6,0.1]
Hub_Ports = [Port(pq.Quantity(150, 'kW')) for i in range(2)]
Hub_Vehicle_Mix = [0.4, 0.5, 0.1]
hub = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix)

def app():

    class_a_mix = st.slider('Vehicle Class A Mix', 0.0, 1.0, Hub_Vehicle_Mix[0], step=0.05,
                                          key="class_a_slider")

    st.metric("Usage 7am-10pm", hub.vehicle_mix[0], round(abs(hub.vehicle_mix[0] - st.session_state.class_a_slider), 2))



