import streamlit as st
import streamlit_toggle as tog

from contents.process import get_chart_1_data, process_chart_1, get_chart_3_4_data, process_chart_3, process_chart_4

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
st.plotly_chart(chart_1)

# CHART 3
chart_3_4_global_data = get_chart_3_4_data() # Loading whole chart data
chart_3 = process_chart_3(chart_3_4_global_data)
st.plotly_chart(chart_3)

# CHART 3
chart_4 = process_chart_4(chart_3_4_global_data)
st.plotly_chart(chart_4)