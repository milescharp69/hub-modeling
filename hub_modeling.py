import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
from Hub import Hub
from Port import Port
from VehicleClass import car
import datetime
import requests
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

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
        "data": ["mi/kWh", "miles/yr", "kWh/yr"],
        "selectedMode": "single",  # Allow only one legend item to be selected at a time
        "selected": {"mi/kWh": True},  # Initially select the "mi/kW" legend item
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
            "name": "mi/kWh",
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
vehicle_explanation_container.markdown("""For the model, the twelve vehicle classes were aggregated into three groups.""")

vehicle_aggregated_chart = {
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "legend": {
        "data": ["mi/kW", "miles/yr"],
        "selectedMode": "single",
        "selected": {"mi/kW": True},
    },
    "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
    "xAxis": {"type": "value"},
    "yAxis": {
        "type": "category",
        "data": [
            "Class 1-2",
            "Class 3-6",
            "Class 7-8",
        ],
    },
    "series": [
        {
            "name": "mi/kW",
            "type": "bar",
            "stack": "total",
            "label": {
                "show": True,
                "position": "inside",
                "color": "black",
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "fontWeight": "normal"
            },
            "emphasis": {"focus": "series"},
            "data": [3.181, 1.245, 0.41],
        },
        {
            "name": "miles/yr",
            "type": "bar",
            "stack": "total",
            "label": {
                "show": True,
                "position": "inside",
                "color": "black",
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "fontWeight": "normal"
            },
            "emphasis": {"focus": "series"},
            "data": [15638, 16200, 48750],
        },
    ],
}

with vehicle_explanation_container:
    st_echarts(options=vehicle_aggregated_chart, height="300px")

# TODO: Complete charging section
# vehicle_charging_container = st.container()
# vehicle_charging_container.subheader("Vehicle Charging")
# # With Battery
# # Without Battery
# if vehicle_charging_container.button('With battery'):
#     vehicle_charging_container.write('Finish')
# else:
#     vehicle_charging_container.write('Finish')

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
              [0.8, 0.6],
              [Port(pq.Quantity(150, 'kW')) for i in range(6)] + [Port(pq.Quantity(350, 'kW')) for i in range(16)] +
               [Port(pq.Quantity(1000, 'kW')) for i in range(18)],
              [0.1, 0.35, 0.55])
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
# Hub Info
# TODO: Finish this

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

# # TODO: Finish explanation how
# vehicle_throughput_explanation_expander = vehicle_throughput_container.expander("Explanation")
# vehicle_throughput_explanation_expander.text("Comeback")

st.title("Simulated Vehicle Throughput")
@st.cache
def hub_sim(_model, date):
    return _model.graphic_sim(date)
df1, df2, df3, df4 = hub_sim(Hub(hub.hub_id, [st.session_state.usage_a_slider, st.session_state.usage_b_slider],
                   hub.hub_ports, [st.session_state.class_a_slider, st.session_state.class_b_slider,
                                   st.session_state.class_c_slider]), "1/31/2022")

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
@st.cache
def estimate_energy(api_key, address, azimuth, tilt, system_capacity, array_type, module_type, losses):
    pvwatts_data = get_pvwatts_data(api_key, address, azimuth=azimuth, tilt=tilt, system_capacity=system_capacity, array_type=array_type, module_type=module_type, losses=losses)

    hours = len(pvwatts_data['outputs']['dc'])
    date_range = pd.date_range(start="2022-01-01", periods=hours, freq="H")
    dc_hourly = pd.Series(pvwatts_data['outputs']['dc'], index=date_range, name="DC Output (W)")

    return dc_hourly

def get_pvwatts_data(api_key, address, system_capacity=4, azimuth=180, tilt=20, array_type=1, module_type=1, losses=14):
    url = 'https://developer.nrel.gov/api/pvwatts/v8'
    params = {
        'format': 'json',
        'api_key': api_key,
        'address': address,
        'system_capacity': system_capacity,
        'azimuth': azimuth,
        'tilt': tilt,
        'array_type': array_type,
        'module_type': module_type,
        'losses': losses,
        'timeframe': 'hourly'  # Add timeframe parameter set to hourly
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return data


#PV Form
with st.form(key='input_form'):
    st.subheader("Enter the required information:")
    address_input = st.text_input("Address:")
    azimuth = st.number_input("Azimuth angle (degrees):", 0, 360, 180)
    tilt = st.number_input("Surface tilt (degrees):", 0, 90, 30)
    system_capacity = st.number_input("System capacity (kW):", 1, 100, 4)
    array_type = st.selectbox("Array type:", [1, 2, 3, 4])
    module_type = st.selectbox("Module type:", [1, 2, 3])
    losses = st.number_input("Losses (%):", 0, 100, 14)
    submit_button = st.form_submit_button("Submit")

# Initialize session state for the figures
if "fig_power" not in st.session_state:
    st.session_state.fig_power = None
if "fig_daily" not in st.session_state:
    st.session_state.fig_daily = None

if submit_button:
    if address_input:
        api_key = 'tOKQdaCJ873TY4aHH8ipheCxZtX86dwvv5fFSPL4'
        dc = estimate_energy(api_key, address_input, azimuth, tilt, system_capacity, array_type, module_type, losses)
        fig_power = px.line(x=dc.index, y=dc, labels={"x": "Date and Time", "y": "DC Output (W)"},
                            title="Hourly DC Output")
        fig_power.update_xaxes(rangeslider_visible=True,
                               rangeselector=dict(buttons=list([
                                   dict(count=1, label="1h", step="hour", stepmode="backward"),
                                   dict(count=6, label="6h", step="hour", stepmode="backward"),
                                   dict(count=12, label="12h", step="hour", stepmode="backward"),
                                   dict(count=24, label="1d", step="hour", stepmode="backward"),
                                   dict(step="all")
                               ])),
                               range=[dc.index[0], dc.index[0] + datetime.timedelta(days=1)])
        # Create an interactive plot with Plotly
        dc_daily = dc.resample("2H").sum() / 1000
        fig = px.line(x=dc_daily.index, y=dc_daily, labels={"x": "Date", "y": "DC Output (kWh)"}, title="Daily DC Output")
        fig.update_xaxes(rangeslider_visible=True,
                         rangeselector=dict(buttons=list([
                             dict(count=1, label="1d", step="day", stepmode="backward"),
                             dict(count=7, label="1w", step="day", stepmode="backward"),
                             dict(count=1, label="1m", step="month", stepmode="backward"),
                             dict(step="all")
                         ])),
                         range=[dc_daily.index[0], dc_daily.index[0] + datetime.timedelta(days=1)])
        st.session_state.fig_power = fig_power
        st.session_state.fig_daily = fig
    else:
        st.error("Invalid address. Please enter a valid address.")

#So figure are not reloaded
if st.session_state.fig_power and st.session_state.fig_daily:
    st.plotly_chart(st.session_state.fig_power)
    st.plotly_chart(st.session_state.fig_daily)

st.title("Cost Estimation")