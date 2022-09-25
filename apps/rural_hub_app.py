import streamlit as st
from streamlit_echarts import st_echarts
import quantities as pq
from Hub import Hub
from Port import Port

#2
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

    # Peak load expander
    # maincol2expander = hubinfocontainercol2.expander("Peak Load", expanded=True)
    # maincol2expander.markdown("<p style='text-align: center; color: black; font-size: 25px;'>{}</p>".format(
    #     Hub_Rural.peak_load), unsafe_allow_html=True)
    #maincol2expander.text("Work In Progress")


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

    #PV /SeSS expander
    # maincol2expander = hubinfocontainercol2.expander("Peak Load", expanded=True)
    # maincol2expander.markdown("<p style='text-align: center; color: black; font-size: 25px;'>{}</p>".format(
    #     Hub_Rural.peak_load), unsafe_allow_html=True)
    # maincol2expander.text("Work In Progress")


    """
    First pass 
    assume for the value of energy produced use 10 cents
    6 cents if you are selling it back t o your rep 
    assume that any given counted vehicle's session is going to take place in 60/150ths of an hour at a given port      What does he mean by this though 
    
    """

    st.title("Simulated Vehicle Throughput")
    #Talk about the assumptions here maybe

    df1, df2, df3, df4 = hub.graphic_sim("1/31/2022")

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


    pv_expander  = st.expander("PV")
    pv_choice = pv_expander.radio("PV Calculation Option", ["Manual", "By offset %"])
    pvform = pv_expander.form("my_form")
    if pv_choice == "Manual":

        pv_infocol1, pv_infocol2 = pvform.columns([1, 1])

        invert_percent = pv_infocol1.number_input("Inverter Loss", 1.10)
        degrad_percent = pv_infocol1.number_input("Degradation Loss", 1.01)
        additional_percent = pv_infocol1.number_input("Additional Losses", 1.00)
        avg_peak_sun_hours = pv_infocol1.number_input("Average Peak Sun Hours", 4.95)

        pv_infocol2.text("Solar Panel Info")
        submit_pv_form = pvform.form_submit_button("Submit")
        panel_wattage = pv_infocol2.number_input("Enter panel wattage (W)", 400)
        panel_length = pv_infocol2.number_input("Enter panel length (m)", 0.9906)
        panel_width = pv_infocol2.number_input("Enter panel width (m)", 1.96)

        panel_area = panel_length * panel_width  # in m^2

        solar_array_output = (energy_consumption * invert_percent * degrad_percent * additional_percent) / (avg_peak_sun_hours)

        panels_needed = (solar_array_output * 1000) / panel_wattage

        required_area = panels_needed * panel_area


    if submit_pv_form:
        pv_col1, pv_col2, pv_col3 = pv_expander.columns([1, 1, 1])

        pv_metric1 = pv_col1.metric("Solar Array Output kW", round(solar_array_output, 3))
        pv_metric2 = pv_col2.metric("Panels Needed", round(panels_needed,3))
        pv_metric3 = pv_col3.metric("Required Area sq m", round(required_area,3))
