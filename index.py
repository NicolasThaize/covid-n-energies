import streamlit as st
import streamlit_toggle as tog
from datetime import datetime

from contents.process import get_chart_1_data, process_chart_1, get_chart_3_4_data, process_chart_3, process_chart_4, get_chart_7_data, process_chart_7

st.set_page_config(layout="wide")
st.title('Data Storytelling Covid19 - Énergies')

# CHART 1
st.header('Nombre de nouveaux cas en France')
chart_1_toggle = tog.st_toggle_switch(
    label="Afficher les lundi, vendredi et samedi", 
    key="Key1", 
    default_value=False, 
    inactive_color = '#D3D3D3', 
    active_color="#11567f", 
    track_color="#29B5E8"
) # Streamlit toggler 
chart_1_global_data = get_chart_1_data(chart_1_toggle) # Loading whole chart data
chart_1 = process_chart_1(chart_1_global_data)
st.plotly_chart(chart_1)

# CHART 3
chart_3_4_global_data = get_chart_3_4_data() # Loading whole chart data
chart_3 = process_chart_3(chart_3_4_global_data)
st.plotly_chart(chart_3)

# CHART 3
chart_4 = process_chart_4(chart_3_4_global_data)
st.plotly_chart(chart_4)
st.plotly_chart(chart_1, use_container_width=True)

# CHART 7
st.header('Production d\'électricité par filière (en MW)')
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Sélectionnez une date de debut",
        datetime(2021, 7, 6))
with col2:
    end_date = st.date_input(
        "Sélectionnez une date de fin",
        datetime(2021, 7, 9))
start_date = start_date.strftime('%Y-%m-%d')
end_date = end_date.strftime('%Y-%m-%d')
chart_7_global_data = get_chart_7_data(start_date, end_date) # Loading whole chart data
chart_7 = process_chart_7(chart_7_global_data, start_date, end_date)
st.plotly_chart(chart_7, use_container_width=True)

