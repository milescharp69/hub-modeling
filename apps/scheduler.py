import streamlit as st
import numpy as np
import quantities as pq
from Hub import Hub
from Port import Port



def app():
    #TODO: User needs to be able to create a custom hub
    #TODO: User needs to be able to create a profile of their vehicle
    #TODO: There needs to be a database that contains the hubs and a database that contains the vehicles


    #Using the selected hub profile and vehicle open up a calendar


    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter some text')
        submit_button = st.form_submit_button(label='Submit')

