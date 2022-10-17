import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
from Hub import Hub
from Port import Port
import pvlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np


def app():
    Hub_Name = "Rural"
    Hub_Notional_Loading = [0.6, 0.1]
    Hub_Ports = [Port(pq.Quantity(150, 'kW')) for i in range(2)]
    Hub_Vehicle_Mix = [0.4, 0.5, 0.1]

    hub = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix)

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

    metric_container_info_col1.metric("Usage 7am-10pm", str(Hub_Notional_Loading[0]),
                                      round(abs(hub.usage_factor[0] - st.session_state.usage_a_slider), 2))
    metric_container_info_col2.metric("Usage 10pm-7am", str(Hub_Notional_Loading[1]),
                                      round(abs(hub.usage_factor[1] - st.session_state.usage_b_slider), 2))

    metric_container_info_col3.metric("Class A Mix", str(Hub_Vehicle_Mix[0]),
                                      round(abs(hub.vehicle_mix[0] - st.session_state.class_a_slider), 2))
    metric_container_info_col4.metric("Class B Mix", str(Hub_Vehicle_Mix[1]),
                                      round(abs(hub.vehicle_mix[1] - st.session_state.class_b_slider), 2))
    metric_container_info_col5.metric("Class C Mix", str(Hub_Vehicle_Mix[2]),
                                      round(abs(hub.vehicle_mix[2] - st.session_state.class_c_slider), 2))

    hub_copy = Hub(Hub_Name, [st.session_state.usage_a_slider, st.session_state.usage_b_slider],
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


    maincol2expander = hubinfocontainercol2.expander("Retail and TDU Charges", expanded=True)
    maincol2expander.text("Work In Progress")


    # Figures

    bargraphexpander = st.expander("Vehicle Throughput")
    hub_max = Hub(Hub_Name, [1, 1], Hub_Ports, Hub_Vehicle_Mix)
    hub_serviced_vehicles = hub.vehicles_serviced()
    hub_max_serviced_vehicles = hub_max.vehicles_serviced()
    hub_copy_serviced_vehicles = hub_copy.vehicles_serviced()

    ####################
    # Bar graph
    #
    #
    if hub_changed:
        BARGRAPH_xaxislabels = ["Typical Use", "Max Use", "Custom Use"]
        BARGRAPH_seriesdata = [{
            "name": "Class A",
            "type": 'bar',
            "stack": 'Ad',
            "emphasis": {
                "focus": 'series'
            },
            "data": [hub_serviced_vehicles[0], hub_max_serviced_vehicles[0], hub_copy_serviced_vehicles[0]]
        },
            {
                "name": "Class B",
                "type": 'bar',
                "stack": 'Ad',
                "emphasis": {
                    "focus": 'series'
                },
                "data": [hub_serviced_vehicles[1], hub_max_serviced_vehicles[1], hub_copy_serviced_vehicles[1]]
            },
            {
                "name": "Class c",
                "type": 'bar',
                "stack": 'Ad',
                "emphasis": {
                    "focus": 'series'
                },
                "data": [hub_serviced_vehicles[2], hub_max_serviced_vehicles[2], hub_copy_serviced_vehicles[2]]
            }

        ]
    else:
        BARGRAPH_xaxislabels = ["Typical Use", "Max Use"]
        BARGRAPH_seriesdata = [{
            "name": "Class A",
            "type": 'bar',
            "stack": 'Ad',
            "emphasis": {
                "focus": 'series'
            },
            "data": [hub_serviced_vehicles[0], hub_max_serviced_vehicles[0]]
        },
            {
                "name": "Class B",
                "type": 'bar',
                "stack": 'Ad',
                "emphasis": {
                    "focus": 'series'
                },
                "data": [hub_serviced_vehicles[1], hub_max_serviced_vehicles[1]]
            },
            {
                "name": "Class c",
                "type": 'bar',
                "stack": 'Ad',
                "emphasis": {
                    "focus": 'series'
                },
                "data": [hub_serviced_vehicles[2], hub_max_serviced_vehicles[2]]
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

    #TODO:come back tot this
    test = bargraphexpander.empty()
    with test:

        st_echarts(options=option)

    """
    First pass 
    assume for the value of energy produced use 10 cents
    6 cents if you are selling it back t o your rep 
    assume that any given counted vehicle's session is going to take place in 60/150ths of an hour at a given port      What does he mean by this though 
    
    """

    st.title("Simulated Vehicle Throughput")
    #Talk about the assumptions here maybe

    @st.cache
    def hub_sim(model, date):
        return model.graphic_sim(date)

    df1, df2, df3, df4 = hub_sim(hub, "1/31/2022")

    simulated_data_graphs = st.expander("Simulated Data Graphs")
    simulated_data_graphs.dataframe(df1)
    simulated_data_graphs.dataframe(df2)
    simulated_data_graphs.dataframe(df3)
    simulated_data_graphs.dataframe(df4)

    power = int(df4["Power"])
    energy_consumption = df3.set_index("Vehicle")["Consumption"]["Class 1-2"] + df3.set_index("Vehicle")["Consumption"]["Class 3-6"] + df3.set_index("Vehicle")["Consumption"]["Class 7-8"]

    st.metric("Power", power)

    sessioncol_ignore1, sessions_graph_col, sessions_chart, sessioncol_ignore2 = st.columns([1, 2, 1, 1])

    with sessions_graph_col:
        options = {
            "xAxis": {
                "type": "category",
                "data": ["Class A", "Class B", "Class C"],
            },
            "yAxis": {"type": "value"},
            "series": [{"data": [df2.set_index("Vehicle")["Sessions"]["Class 1-2"],
                                 df2.set_index("Vehicle")["Sessions"]["Class 3-6"],
                                 df2.set_index("Vehicle")["Sessions"]["Class 7-8"]], "type": "bar"}],
        }
        st_echarts(options=options)
    sessions_chart.metric("Class A",df2.set_index("Vehicle")["Sessions"]["Class 1-2"])
    sessions_chart.metric("Class B", df2.set_index("Vehicle")["Sessions"]["Class 3-6"])
    sessions_chart.metric("Class C", df2.set_index("Vehicle")["Sessions"]["Class 7-8"])


    st.title("PV")

    #Solar panel DataBase
    cec_mod_db = pvlib.pvsystem.retrieve_sam('CECmod')

    # Inverter Database
    invert_df = pvlib.pvsystem.retrieve_sam('CECInverter')

    pv_advanced_form = st.form("pv_ad_form")

    # Coordinates of the weather station at University of Oregon (SRML)
    pv_location_expander = pv_advanced_form.expander("Location")

    #TODO: Input address and then convert to latitude and longitude

    latitude = pv_location_expander.number_input("Latitude", 44.0467)
    longitude = pv_location_expander.number_input("Longitude", -123.0743)
    altitude = pv_location_expander.number_input("Altitude", 133.8)
    surface_tilt = pv_location_expander.number_input("Surface Tilt", 30)
    surface_azimuth = pv_location_expander.number_input("Surface Azimuth", 180)
    location = pvlib.location.Location(latitude, longitude, altitude=altitude)  # Define the location object

    #TODO: Get correct station id based on location information
    with st.spinner('Loading...'):
        #Weather df
        df_weather = pvlib.iotools.read_midc_raw_data_from_nrel('UOSMRL',  # Station id
                                                                pd.Timestamp('20210601'),  # Start date YYYYMMDD
                                                                pd.Timestamp('20210601'))  # End date  YYYYMMDD
        df_weather = df_weather[['Global CMP22 [W/m^2]', 'Diffuse Schenk [W/m^2]',
                                 'Direct CHP1 [W/m^2]', 'Air Temperature [deg C]', 'Avg Wind Speed @ 10m [m/s]']]
        df_weather_copy = df_weather.copy()

        df_weather.columns = ['ghi', 'dhi', 'dni', 'temp_air', 'wind_speed']
        weather_data_expander = pv_advanced_form.expander("Weather Data", expanded=False)
        weather_data_expander.dataframe(df_weather_copy)


        #Get Solar panel
        module_data = cec_mod_db.iloc[:, 0] # Define the PV Module and the Inverter from the CEC databases (For example, the first entry of the databases)

        module_data_expander = pv_advanced_form.expander("Solar Panel Data", expanded=False)
        module_data_expander.dataframe(module_data)

        #Get Inverter
        inverter_data = invert_df["ABB__PVI_3_0_OUTD_S_US__208V_"]

        inverter_model_expander = pv_advanced_form.expander("Inverter Data", expanded=False)
        inverter_model_expander.dataframe(inverter_data)

        submit_pv_form = pv_advanced_form.form_submit_button("Submit")

    if submit_pv_form:
        with st.spinner('Loading...'):
            #TODO: Double check what this is
            # Define Temperature Paremeters
            temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm'][
                'open_rack_glass_glass']
            # Define the basics of the class PVSystem
            system = pvlib.pvsystem.PVSystem(surface_tilt=surface_tilt,
                                             surface_azimuth=surface_azimuth,
                                             module_parameters=module_data,
                                             inverter_parameters=inverter_data,
                                             temperature_model_parameters=temperature_model_parameters,
                                             modules_per_string=10,
                                             strings_per_inverter=10
                                             )

            # Creation of the ModelChain object
            """ The example does not consider AOI losses nor irradiance spectral losses"""
            mc = pvlib.modelchain.ModelChain(system, location,
                                             aoi_model='no_loss',
                                             spectral_model='no_loss',
                                             name='AssessingSolar_PV')
            mc.run_model(df_weather)

            # Plot of Power Output
            fig, ax = plt.subplots(figsize=(7, 3))

            mc.results.dc['p_mp'].plot(label='DC power')
            print(mc.results.dc['p_mp'])
            print(type(mc.results.dc['p_mp']))
            ax = mc.results.ac.plot(label='AC power')

            ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
            ax.set_ylabel('Power [W]')
            ax.set_xlabel('UTC Time [HH:MM]')
            ax.set_title('Power Output of PV System')
            plt.legend()
            plt.tight_layout()
            plt.show()
            st.pyplot(fig)

            # Estimate solar energy available and generated
            poa_energy = mc.results.total_irrad['poa_global'].sum() * (1 / 60) / 1000  # Daily POA irradiation in kWh
            dc_energy = mc.results.dc['p_mp'].sum() * (1 / 60) / 1000  # Daily DC energy in kWh
            ac_energy = mc.results.ac.sum() * (1 / 60) / 1000  # Daily AC energy in kWh

            print('*' * 15, ' Daily Production ', '*' * 15, '\n', '-' * 48)
            print('\tPOA irradiation: ', "%.2f" % poa_energy, 'kWh')
            print('\tInstalled PV Capacity: ', "%.2f" % module_data['STC'], 'W')
            print('\tDC generation:', "%.2f" % dc_energy, 'kWh (', '%.2f' % (dc_energy * 1000 / module_data['STC']),
                  'kWh/kWp)')
            print('\tAC generation:', "%.2f" % ac_energy, 'kWh (', '%.2f' % (ac_energy * 1000 / module_data['STC']),
                  'kWh/kWp)')
            print('-' * 50)

    #Offset slider for cost?
