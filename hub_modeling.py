import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
from Hub import Hub
from Port import Port
import pvlib
import pandas as pd
from pvlib import location
from pvlib import irradiance
from pvlib import pvsystem
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from VehicleClass import car
import datetime
import geopy
from timezonefinder import TimezoneFinder
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
from haversine import haversine, Unit
import requests
import io
import numpy as np
st.title("Hub Model Explanation")

# TODO:Finish explanation
model_explanation = st.container()

# Create a container for the vehicle explanation section
vehicle_explanation_container = st.container()

# Add a subheader for the vehicle explanation section
vehicle_explanation_container.subheader("Vehicle Explanation")

# Add a comment about the vehicle classes used in the model
vehicle_classes_comment = "The following twelve vehicle classes were used in this model:"
vehicle_classes_expander = vehicle_explanation_container.expander(vehicle_classes_comment)
# Create an ECharts chart to display the twelve vehicle classes
vehicle_classes_chart = {
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "legend": {
        "data": ["mi/kW", "miles/yr", "kWh/yr"],
        "selectedMode": "single",  # Allow only one legend item to be selected at a time
        "selected": {"mi/kW": True},  # Initially select the "mi/kW" legend item
    },
    "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
    "xAxis": {"type": "value"},
    "yAxis": {
        "type": "category",
        "data": [
            "Sedan Average",
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
            "Class8 (freight)",
        ],
    },
    "series": [
        {
            "name": "mi/kW",
            "type": "bar",
            "stack": "total",
            "label": {
                "show": True,
                "position": "outsideRight"
            },
            "emphasis": {"focus": "series"},
            "data": [3.8, 3.9, 3.8, 3, 2, 1.5, 0.65, 0.65, 0.5, 0.5, 0.4, 0.35],
        },
        {
            "name": "miles/yr",
            "type": "bar",
            "stack": "total",
            "label": {
                "show": True,
                "position": "outsideRight"
            },
            "emphasis": {"focus": "series"},
            "data": [16100, 8000, 45000, 16100, 14000, 12000, 12000, 40000, 25000, 40000, 50000, 60000],
        },
        {
            "name": "kWh/yr",
            "type": "bar",
            "stack": "total",
            "label": {
                "show": True,
                "position": "outsideRight"
            },
            "emphasis": {"focus": "series"},
            "data": [4237, 2051, 11842, 5367, 7000, 8000, 18462, 61538, 50000, 80000, 125000, 171429],
        },
    ],
}
# Create an empty expander to hold the ECharts chart
vehicle_classes_chart_expander = vehicle_classes_expander.empty()
# Add the ECharts chart to the expander
with vehicle_classes_chart_expander:
    st_echarts(options=vehicle_classes_chart, height="500px")
"""For the model, the twelve vehicle classes were aggregated into three groups. """
#TODO:Finish the vehicle aggregated graph

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

# TODO: Complete charging section
vehicle_charging_container = st.container()
vehicle_charging_container.subheader("Vehicle Charging")
# With Battery
# Without Battery
if vehicle_charging_container.button('With battery'):
    vehicle_charging_container.write('Finish')
else:
    vehicle_charging_container.write('Finish')

# Sidebar code
hub_types = ["Rural", "Commercial Dominant", 'Urban Community', "Urban Multimodal"]

selected_hub_type = st.sidebar.selectbox(
    'Hub Type',
    hub_types
)

# Hub Types
if selected_hub_type == "Rural":
    hub = Hub(selected_hub_type,
              [0.6, 0.1],
              [Port(pq.Quantity(150, 'kW')) for i in range(2)],
              [0.4, 0.5, 0.1])
elif selected_hub_type == "Commercial Dominant":
    hub = Hub(selected_hub_type,
              [0.6, 0.1],
              [Port(pq.Quantity(150, 'kW')) for i in range(6)] + [Port(pq.Quantity(350, 'kW')) for i in range(18)] +
               [Port(pq.Quantity(350, 'kW')) for i in range(16)],
              [0.4, 0.5, 0.1])
elif selected_hub_type == "Urban Community":
    hub = Hub(selected_hub_type,
              [0.7, 0.5],
              [Port(pq.Quantity(150, 'kW')) for i in range(2)],
              [0.7, 0.3, 0.0])
elif selected_hub_type == "Urban Multimodal":
    hub = Hub(selected_hub_type,
              [0.7, 0.5],
              [Port(pq.Quantity(150, 'kW')) for i in range(8)] + [Port(pq.Quantity(300, 'kW')) for i in range(2)] ,
              [0.35, 0.5, 0.15])

#Hub info expander
hubinfocontainer = st.sidebar.container()
hubinfoexpander = hubinfocontainer.expander("Hub Information ", expanded=True)
hubinfoexpander.markdown(
    """
<style>
.streamlit-expanderHeader {
    font-size: x-large;
}
</style>
""",
    unsafe_allow_html=True,
)
hubinfoexpander.markdown(
    "<p style='text-align: left; color: black; text-indent: 15%;'>Hub Type:       {}</p>".format(
        hub.hub_id), unsafe_allow_html=True)
hubinfoexpander.markdown(
    "<p style='text-align: left; color: black; text-indent: 15%;'>Total Ports:        {}</p>".format(
        hub.total_ports), unsafe_allow_html=True)
hubinfoexpander.markdown(
    "<p style='text-align: left; color: black; text-underline-offset: 20%; text-indent: 15%;'><u>Types of Ports</u></p>",
    unsafe_allow_html=True)
for i in hub.port_types.keys():
    hubinfoexpander.markdown(
        "<p style='text-align: left; color: black; text-underline-offset: 20%; text-indent: 20%;'>• {}</p>".format(
            str(int(i)) + "kW x " + str(hub.port_types[i])),
        unsafe_allow_html=True)

retail_charge_expander = st.sidebar.expander("Retail and TDU Charges")
pq.markup.config.use_unicode = True
unitsDollars = pq.UnitQuantity('USD', 1, symbol='$')
# initialize a list to store the charges
charges = []
if "charges" not in st.session_state:
    st.session_state.charges = []
# define a function to add a new charge to the list
def add_charge(name, cost, unit):
    charge = {
        'name': name,
        'cost': cost,
        'unit': unit
    }
    st.session_state.charges.append(charge)

# define a function to display the charges as a table
def display_charges():
    total_cost = 0
    for charge in st.session_state.charges:
        total_cost += charge['cost']
    retail_charge_expander.write(f"Total cost of charges: ${total_cost:.2f}")
    retail_charge_expander.write("Charges:")
    for i, charge in enumerate(st.session_state.charges):
        retail_charge_expander.write(f"{i+1}. {charge['name']}: {charge['cost']:.2f} {charge['unit']}")


# define input fields for adding a new charge
new_charge_name = retail_charge_expander.text_input("Charge name")
new_charge_cost = retail_charge_expander.number_input("Charge cost")
new_charge_unit = retail_charge_expander.selectbox("Charge unit", ["USD / kWh", "USD / kW"])
# add the new charge to the list when the "Add charge" button is clicked
if retail_charge_expander.button("Add charge"):
    add_charge(new_charge_name, new_charge_cost, new_charge_unit)
    # clear the input fields for the next charge
    new_charge_name = ""
    new_charge_cost = 0
    new_charge_unit = "USD / kWh"
# display the current charges as a table
display_charges()


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
    # TODO: Prevent the site for loading anything
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

energy_consumption = 0.0
for vehicle_class in ["Class 1-2", "Class 3-6", "Class 7-8"]:
    try:
        energy_consumption += df3.set_index("Vehicle")["Consumption"][vehicle_class]
    except KeyError:
        pass

st.metric("Power", power)

session_data = np.zeros(3)

for i, vehicle_class in enumerate(["Class 1-2", "Class 3-6", "Class 7-8"]):
    try:
        session_data[i] = df2.set_index("Vehicle")["Sessions"][vehicle_class]
    except KeyError:
        pass

options = {
    "xAxis": {
        "type": "category",
        "data": ["Class A", "Class B", "Class C"],
    },
    "yAxis": {"type": "value"},
    "series": [{"data": session_data.tolist(), "type": "bar"}],
}
sessioncol_ignore1, sessions_graph_col, sessions_chart, sessioncol_ignore2 = st.columns([1, 2, 1, 1])

with sessions_graph_col:
    st_echarts(options=options)

for i, vehicle_class in enumerate(["Class 1-2", "Class 3-6", "Class 7-8"]):
    try:
        sessions_chart.metric(vehicle_class, df2.set_index("Vehicle")["Sessions"][vehicle_class])
    except KeyError:
        sessions_chart.metric(vehicle_class, 0)






#Solar Panel
st.title("PV Energy Estimation")
def get_location(address):
    geolocator = Nominatim(user_agent="pv_energy_estimator")
    max_retries = 3
    timeout = 1

    for i in range(max_retries):
        try:
            location = geolocator.geocode(address, timeout=timeout)
            if location is not None:
                latitude = location.latitude
                longitude = location.longitude
                timezone = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
                return pvlib.location.Location(latitude, longitude, tz=timezone)
            else:
                return None
        except (GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError):
            timeout *= 2  # Increase the timeout for the next attempt

    return None
def estimate_energy(site, azimuth, tilt, module, inverter, weather_data):
    # Define Temperature Paremeters
    temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm'][
        'open_rack_glass_glass']
    # Define the basics of the class PVSystem
    system = pvlib.pvsystem.PVSystem(surface_tilt=tilt,
                                     surface_azimuth=azimuth,
                                     module_parameters=module,
                                     inverter_parameters=inverter,
                                     temperature_model_parameters=temperature_model_parameters
                                     )
    # Creation of the ModelChain object
    """ The example does not consider AOI losses nor irradiance spectral losses"""
    mc = pvlib.modelchain.ModelChain(system, site,
                                     aoi_model='no_loss',
                                     spectral_model='no_loss',
                                     name='AssessingSolar_PV')
    mc.run_model(weather_data)
    # Plot the DC power output as a function of time
    fig, ax = plt.subplots(figsize=(7, 3))
    mc.results.dc['p_mp'].plot(ax=ax, label='DC Power Output')
    ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
    ax.set_ylabel('Power (W)')
    ax.set_xlabel('Time (UTC)')
    ax.set_title('DC Power Output of PV System')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

    # Calculate the daily energy generation and plot it as a function of time
    dc_energy = mc.results.dc['p_mp'] / 60.0 / 1000.0  # convert from W to kWh
    daily_energy = dc_energy.resample('D').sum()

    fig, ax = plt.subplots(figsize=(7, 3))
    daily_energy.plot(ax=ax, label='Daily Energy Generation')
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    ax.set_ylabel('Energy (kWh)')
    ax.set_xlabel('Date (UTC)')
    ax.set_title('Daily Energy Generation of PV System')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

    return dc_energy
def get_station_data():
    api_key = 'tOKQdaCJ873TY4aHH8ipheCxZtX86dwvv5fFSPL4'  # Replace with your NREL API Key
    url = f'https://developer.nrel.gov/api/midc_stations/v1.json?api_key={api_key}'
    response = requests.get(url)

    if response.status_code == 404:
        raise Exception("API request returned 404 Not Found. Please check the API endpoint URL and parameters.")

    data = response.json()
    return pd.DataFrame(data['stations'])
def get_nsrdb_data(latitude, longitude, start_date, end_date, api_key):
    url = 'https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv'
    params = {
        'wkt': f'POINT({longitude} {latitude})',
        'names': f'{start_date.year}',
        'leap_day': 'false',
        'interval': '60',
        'utc': 'false',
        'full_name': 'Miles Charpentier',
        'email': 'miles.charpentier.amaz@gmail.com',
        'affiliation': 'Student',
        'mailing_list': 'false',
        'reason': 'research',
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    weather_data = pd.read_csv(io.StringIO(response.text), skiprows=[0, 1])
    weather_data.to_csv("weather_data.csv", index=False)
    weather_data['Time'] = pd.to_datetime(weather_data.index)
    weather_data = weather_data.set_index('Time')
    weather_data = weather_data[['GHI', 'DNI', 'DHI', 'Temperature', 'Wind Speed']]
    weather_data.columns = ['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed']
    #dni_extra represents the extraterrestrial direct normal irradiance
    weather_data["dni_extra"] = pvlib.irradiance.get_extra_radiation(weather_data.index)

    return weather_data

#TODO: Fix it
#PV Form
with st.form(key='input_form'):
    st.subheader("Enter the required information:")
    address_input = st.text_input("Address:")
    azimuth = st.number_input("Azimuth angle (degrees):", 0, 360, 180)
    tilt = st.number_input("Surface tilt (degrees):", 0, 90, 30)

    sandia_modules = pvlib.pvsystem.retrieve_sam("SandiaMod")
    sandia_inverters = pvlib.pvsystem.retrieve_sam("sandiainverter")

    module_input = st.selectbox("PV module:", list(sandia_modules.columns))
    inverter_input = st.selectbox("Inverter:", list(sandia_inverters.columns))

    module_expander = st.expander("PV Module Information", expanded=False)
    with module_expander:
        st.write(sandia_modules[module_input])

    inverter_expander = st.expander("Inverter Information", expanded=False)
    with inverter_expander:
        st.write(sandia_inverters[inverter_input])

    submit_button = st.form_submit_button("Submit")
if submit_button:
    site = get_location(address_input)

    if site is not None:
        st.write(f"Location (latitude, longitude): {site.latitude}, {site.longitude}")
        st.write(f"Timezone: {site.tz}")

        module = sandia_modules[module_input]
        inverter = sandia_inverters[inverter_input]

        start_date = pd.Timestamp('2020-01-01', tz='UTC')
        end_date = pd.Timestamp('2020-1-02', tz= 'UTC')
        api_key = 'tOKQdaCJ873TY4aHH8ipheCxZtX86dwvv5fFSPL4'


        weather_data = get_nsrdb_data(site.latitude, site.longitude, start_date, end_date, api_key)

        energy = estimate_energy(site, azimuth, tilt, module, inverter, weather_data)

    else:
        st.error("Invalid address. Please enter a valid address.")