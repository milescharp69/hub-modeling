import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
from Hub import Hub
from Port import Port
import pvlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from VehicleClass import car
import datetime
import geopy
import timezonefinder, pytz

st.title("Hub Model Explanation")

# TODO:Finish explanation
model_explanation = st.container()

vehicle_explanation_container = st.container()
vehicle_explanation_container.subheader("Vehicle Explanation")
"""The following vehicle classes were used in this model"""
vehicle_explanation_twelve_class_chart = vehicle_explanation_container.expander("The Twelve Vehicle Classes")

options = {
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "legend": {
        "data": ["mi/kW", "miles/yr", "kWh/yr"]
    },
    "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
    "xAxis": {"type": "value"},
    "yAxis": {
        "type": "category",
        "data": ["Sedan Average",
                 "Sedan (Urban/Low)",
                 "Sedan High/Rideshare",
                 "SUV",
                 "PU/Van (Class 1-2)",
                 "Class3/4 (SmBox, Minibus)",
                 "Class5/6 (School,Bucket: L)",
                 "Class5/6 (School,Bucket: H)",
                 "Class7 (Refuse, Transit: L)",
                 "Class7 (Refuse, Transit: H)",
                 "Class8 (local)",
                 "Class8 (freight)"]
    },
    "series": [
        {
            "name": "mi/kW",
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [3.8, 3.9, 3.8, 3, 2, 1.5, 0.65, 0.65, 0.5, 0.5, 0.4, 0.35],
        },
        {
            "name": "miles/yr",
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [16100, 8000, 45000, 16100, 14000, 12000, 12000, 40000, 25000, 40000, 50000, 60000],
        },
        {
            "name": "kWh/yr",
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [4237, 2051, 11842, 5367, 7000, 8000, 18462, 61538, 50000, 80000, 125000, 171429],
        }

    ],
}

vehicle_explanation_twelve_class_chart_empty = vehicle_explanation_twelve_class_chart.empty()
with vehicle_explanation_twelve_class_chart_empty:
    st_echarts(options=options, height="500px")

"""For the model, the twelve vehicle classes were aggregated into three groups. """

# if veh_class == 0:
#     self.mi_kWH = pq.Quantity(3.181, 'miles / (kW * hour)')
#     self.mi_year = pq.Quantity(15638, 'miles / year')
#     self.className = 'Class 1-2'
# elif veh_class == 1:
#     self.mi_kWH = pq.Quantity(1.245, 'miles / (kW * hour)')
#     self.mi_year = pq.Quantity(16200, 'miles / year')
#     self.className = 'Class 3-6'
# else:
#     self.mi_kWH = pq.Quantity(0.41, 'miles / (kW * hour)')
#     self.mi_year = pq.Quantity(48750, 'miles / year')
#     self.className = 'Class 7-8'


# Battery
# M
# TODO: Complete charging section
vehicle_charging_container = st.container()
vehicle_charging_container.subheader("Vehicle Charging")

if vehicle_charging_container.button('With battery'):
    vehicle_charging_container.write('Why hello there')
else:
    vehicle_charging_container.write('Goodbye')

# With Battery
# Without Battery

[car(pq.Quantity(85, 'kW'), 0),
 car(pq.Quantity(225, 'kW'), 1),
 car(pq.Quantity(525, 'kW'), 2)]

# Sidebar code
hub_types = ["Rural", "Commercial Dominant", 'Urban Community', "Urban Multimodal"]

selected_hub_type = st.sidebar.selectbox(
    'Hub Type',
    hub_types
)

# TODO: Finish adding all the parameters for each hub
# Hub Types
if selected_hub_type == "Rural":
    hub = Hub(selected_hub_type,
              [0.6, 0.1],
              [Port(pq.Quantity(150, 'kW')) for i in range(2)],
              [0.4, 0.5, 0.1])
elif selected_hub_type == "Commercial Dominant":
    hub = Hub(selected_hub_type,
              [0.6, 0.1],
              [Port(pq.Quantity(150, 'kW')) for i in range(2)],
              [0.4, 0.5, 0.1])

    # Hub_Name = "Rural"
    # Hub_Notional_Loading = [0.6, 0.1]
    # # np.array([Port(pq.Quantity(150, 'kW'),6), Port(pq.Quantity(350, 'kW'),18),Port(pq.Quantity(1000, 'kW'),16)])
    # Hub_Ports = [Port(pq.Quantity(150, 'kW')) for i in range(2)]
    # Hub_Vehicle_Mix = [0.4, 0.5, 0.1]
    #
    # Vehicle_Classes = [Class_A, Class_B, Class_C]
    # Hub_Commercial_Dominant = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)
elif selected_hub_type == "Urban Community":
    hub = Hub(selected_hub_type,
              [0.6, 0.1],
              [Port(pq.Quantity(150, 'kW')) for i in range(2)],
              [0.4, 0.5, 0.1])

    # Hub_Name = "Urban Community"
    # Hub_Notional_Loading = [0.7, 0.5]
    # Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'), 2)])
    # Hub_Vehicle_Mix = [0.7, 0.3, 0]
    # Vehicle_Classes = [Class_A, Class_B, Class_C]
    # Hub_Urban_Community = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)
elif selected_hub_type == "Urban Multimodal":
    hub = Hub(selected_hub_type,
              [0.6, 0.1],
              [Port(pq.Quantity(150, 'kW')) for i in range(2)],
              [0.4, 0.5, 0.1])
    # Hub_Name = "Urban Multimodal"
    # Hub_Notional_Loading = [0.7, 0.5]
    # Hub_Ports = np.array([Port(pq.Quantity(150, 'kW'), 8), Port(pq.Quantity(300, 'kW'), 2)])
    # Hub_Vehicle_Mix = [0.35, 0.5, 0.15]
    # Vehicle_Classes = [Class_A, Class_B, Class_C]
    # Hub_Urban_Multimodal = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

# Hub Info
# TODO: Finish this

# Hubinfo expander
hubinfocontainer = st.sidebar.container()
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
            str(int(i)) + "kW x " + str(hub.port_types[i])),
        unsafe_allow_html=True)

maincol2expander = hubinfocontainercol2.expander("Retail and TDU Charges", expanded=True)
maincol2expander.text("Work In Progress")

# Class Mixes
classmix_expander = st.sidebar.expander("Vehicle Class Mix Sliders")

classmix_sliders, classmix_metrics = classmix_expander.columns([1, 1], gap="large")

class_a_mix = classmix_sliders.slider('Vehicle Class A Mix', 0.0, 1.0, hub.vehicle_mix[0], step=0.05,
                                      key="class_a_slider")
classmix_metrics.metric("Class A Mix", str(hub.vehicle_mix[0]),
                        round(abs(hub.vehicle_mix[0] - st.session_state.class_a_slider), 2))
class_b_mix = classmix_sliders.slider('Vehicle Class B Mix', 0.0, 1.0, hub.vehicle_mix[1], step=0.05,
                                      key="class_b_slider")
classmix_metrics.metric("Class B Mix", str(hub.vehicle_mix[1]),
                        round(abs(hub.vehicle_mix[1] - st.session_state.class_b_slider), 2))
class_c_mix = classmix_sliders.slider('Vehicle Class C Mix', 0.0, 1.0, hub.vehicle_mix[2], step=0.05,
                                      key="class_c_slider")
classmix_metrics.metric("Class C Mix", str(hub.vehicle_mix[2]),
                        round(abs(hub.vehicle_mix[2] - st.session_state.class_c_slider), 2))

if class_a_mix + class_b_mix + class_c_mix != 1:
    # TODO: Find a way to prevent the site for loading anything

    # update Vehicle mix
    classmix_expander.text("Vehicle Mix should add up to 1!")

# Usage Factor Side Bar
usage_factor_expander = st.sidebar.expander("Usage Factor")

usage_factor_sliders, usage_factor_metrics = usage_factor_expander.columns([1, 1], gap="large")

sliderUsageA = usage_factor_sliders.slider('Usage 7am-10pm', 0.0, 1.0, hub.usage_factor[0], step=0.05,
                                           key="usage_a_slider")
usage_factor_metrics.metric("Usage 7am-10pm", str(hub.usage_factor[0]),
                            round(abs(hub.usage_factor[0] - st.session_state.usage_a_slider), 2))

sliderUsageB = usage_factor_sliders.slider('Usage 10pm-7am', 0.0, 1.0, hub.usage_factor[1], step=0.05,
                                           key="usage_b_slider")
usage_factor_metrics.metric("Usage 10pm-7am", str(hub.usage_factor[1]),
                            round(abs(hub.usage_factor[1] - st.session_state.usage_b_slider), 2))

hub_copy = Hub(hub.hub_id, [st.session_state.usage_a_slider, st.session_state.usage_b_slider],
               hub.hub_ports, [st.session_state.class_a_slider, st.session_state.class_b_slider,
                               st.session_state.class_c_slider])

# Check is hub was changed
if hub.usage_factor != hub_copy.usage_factor or hub.vehicle_mix != hub_copy.vehicle_mix:
    hub_changed = True
elif hub.usage_factor == hub_copy.usage_factor or hub.vehicle_mix == hub_copy.vehicle_mix:
    hub_changed = False

# Figures
vehicle_throughput_container = st.container()
vehicle_throughput_container.subheader("Vehicle Throughput")
vehicle_throughput_container.text("This section calculates the maximum throughput a given hub could service.")
vehicle_throughput_expander = vehicle_throughput_container.expander("Throughput")
hub_max = Hub(hub.hub_id, [1, 1], hub.hub_ports, hub.vehicle_mix)
hub_serviced_vehicles = hub.vehicles_serviced()
hub_max_serviced_vehicles = hub_max.vehicles_serviced()
hub_copy_serviced_vehicles = hub_copy.vehicles_serviced()

####################
# Bar graph
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

test = vehicle_throughput_expander.empty()
with test:
    st_echarts(options=option)

# TODO: Finish explanation how
vehicle_throughput_explanation_expander = vehicle_throughput_container.expander("Explanation")
vehicle_throughput_explanation_expander.text("Comeback")

#
# """
# First pass
# assume for the value of energy produced use 10 cents
# 6 cents if you are selling it back t o your rep
# assume that any given counted vehicle's session is going to take place in 60/150ths of an hour at a given port      What does he mean by this though
#
# """

st.title("Simulated Vehicle Throughput")


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
energy_consumption = df3.set_index("Vehicle")["Consumption"]["Class 1-2"] + df3.set_index("Vehicle")["Consumption"][
    "Class 3-6"] + df3.set_index("Vehicle")["Consumption"]["Class 7-8"]

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
sessions_chart.metric("Class A", df2.set_index("Vehicle")["Sessions"]["Class 1-2"])
sessions_chart.metric("Class B", df2.set_index("Vehicle")["Sessions"]["Class 3-6"])
sessions_chart.metric("Class C", df2.set_index("Vehicle")["Sessions"]["Class 7-8"])

# Solar Panel

st.title("PV")

pv_container = st.container()

pv_advanced_form = pv_container.form("pv_ad_form")

tab1, tab2, tab3, tab4 = pv_advanced_form.tabs(["Location", "Weather Data", "Solar Panel Data", "Inverter Data"])

# TODO: Check back we might need to cache these
cec_mod_db = pvlib.pvsystem.retrieve_sam('CECmod')  # Solar panel DataBase
invert_df = pvlib.pvsystem.retrieve_sam('CECInverter')  # Inverter Database


# TODO: Add a try and except here

#Location Handling
address = tab1.text_input('Address of PV System, Example: Champ de Mars, Paris, France')
surface_tilt = tab1.number_input("Surface Tilt", 30)
surface_azimuth = tab1.number_input("Surface Azimuth", 180)

locator = geopy.Nominatim(user_agent="myGeocoder")
tf = timezonefinder.TimezoneFinder()
location = locator.geocode(address)
longitude, latitude, altitude = location.longitude, location.latitude, location.altitude

@cache
def get_location(lat, long):



def get_tz():
    try:
        timezone_str = tf.certain_timezone_at(lat=latitude, lng=longitude)

        if timezone_str is None:
            raise Exception("Could not determine the time zone")
        else:
            # Display the current time in that time zone
            timezone = pytz.timezone(timezone_str)
            dt = datetime.datetime.utcnow()
            print("The time in %s is %s" % (timezone_str, dt + timezone.utcoffset(dt)))
    except Exception as inst:
        e = inst.args
        if e == "Could not determine the time zone":
            print("")






# Define the location object
location = pvlib.location.Location(latitude=latitude, longitude=longitude, altitude=altitude, tz= timezone_str)

# TODO: Get correct station id based on location information
# TODO: Cache this so it does not have to reload every time

# Weather df
df_weather = pvlib.iotools.read_midc_raw_data_from_nrel('UOSMRL',  # Station id
                                                        pd.Timestamp('20210601'),  # Start date YYYYMMDD
                                                        pd.Timestamp('20210601'))  # End date  YYYYMMDD
df_weather = df_weather[['Global CMP22 [W/m^2]', 'Diffuse Schenk [W/m^2]',
                         'Direct CHP1 [W/m^2]', 'Air Temperature [deg C]', 'Avg Wind Speed @ 10m [m/s]']]
df_weather_copy = df_weather.copy()

df_weather.columns = ['ghi', 'dhi', 'dni', 'temp_air', 'wind_speed']

tab2.dataframe(df_weather_copy)

# Get Solar panel
# Define the PV Module and the Inverter from the CEC databases (For example, the first entry of the databases)
module_data = cec_mod_db.iloc[:, 0]

tab3.dataframe(module_data)

# Get Inverter
inverter_data = invert_df["ABB__PVI_3_0_OUTD_S_US__208V_"]

tab4.dataframe(inverter_data)

submit_pv_form = pv_advanced_form.form_submit_button("Submit")

if submit_pv_form:
    with st.spinner('Loading...'):
        # TODO: Double check what this is
        # Define Temperature Paremeters
        temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm'][
            'open_rack_glass_glass']
        # Define the basics of the class PVSystem
        system = pvlib.pvsystem.PVSystem(surface_tilt=surface_tilt,
                                         surface_azimuth=surface_azimuth,
                                         module_parameters=module_data,
                                         inverter_parameters=inverter_data,
                                         temperature_model_parameters=temperature_model_parameters
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
        # ac_energy = mc.results.ac.sum() * (1 / 60) / 1000  # Daily AC energy in kWh

        print('*' * 15, ' Daily Production ', '*' * 15, '\n', '-' * 48)
        print('\tPOA irradiation: ', "%.2f" % poa_energy, 'kWh')
        print('\tInstalled PV Capacity: ', "%.2f" % module_data['STC'], 'W')
        print('\tDC generation:', "%.2f" % dc_energy, 'kWh (', '%.2f' % (dc_energy * 1000 / module_data['STC']),
              'kWh/kWp)')
        # print('\tAC generation:', "%.2f" % ac_energy, 'kWh (', '%.2f' % (ac_energy * 1000 / module_data['STC']),
        #       'kWh/kWp)')
        # print('-' * 50)

        st.dataframe(mc.results.dc['p_mp'])
