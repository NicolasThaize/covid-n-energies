import streamlit as st
import streamlit_toggle as tog

from contents.process import get_chart_1_data, process_chart_1, get_chart_7_data, process_chart_7

st.set_page_config(layout="wide")
st.title('Data Storytelling Covid19 - Énergies')

# CHART 1
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
st.plotly_chart(chart_1, use_container_width=True)

# CHART 7
chart_7_global_data = get_chart_7_data() # Loading whole chart data
chart_7 = process_chart_7(chart_7_global_data)
st.plotly_chart(chart_7, use_container_width=True)
