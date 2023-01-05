import streamlit as st
import streamlit_toggle as tog
from datetime import datetime
from contents.process import get_chart_1_data, process_chart_1, get_chart_3_4_data, process_chart_3, process_chart_4, get_chart_7_data, process_chart_7, process_chart_10, process_chart_8_9, get_chart_8_9_data
from contents.sides import get_covid_phases_labels_in_list
from contents.utils import compare_with_year

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
st.plotly_chart(chart_1, use_container_width=True)

# CHART 3
st.header('Consommation brute d\'électricté en France (en MW)')
chart_3_4_global_data = get_chart_3_4_data() # Loading whole chart data
chart_3 = process_chart_3(chart_3_4_global_data)
st.plotly_chart(chart_3, use_container_width=True)

# CHART 3
st.header('Consommation brute de gaz en France (en MW)')
chart_4 = process_chart_4(chart_3_4_global_data)
st.plotly_chart(chart_4, use_container_width=True)

# CHART 7
st.header('Production d\'électricité par filière (en MW)')
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Sélectionnez une date de debut",
        datetime(2020, 10, 29),
        min_value=datetime(2019, 1, 1),
        max_value=datetime(2022, 12, 28))
with col2:
    end_date = st.date_input(
        "Sélectionnez une date de fin",
        datetime(2020, 12, 15),
        min_value=datetime(2019, 1, 1),
        max_value=datetime(2022, 12, 28))
start_date = start_date.strftime('%Y-%m-%d')
end_date = end_date.strftime('%Y-%m-%d')
chart_7_global_data = get_chart_7_data(start_date, end_date) # Loading whole chart data
chart_7 = process_chart_7(chart_7_global_data, start_date, end_date)
st.plotly_chart(chart_7, use_container_width=True)

# CHART 8 9
st.header('Evolution de la part de la consommation d\'énergie brute (en %)')
chart_8_9_data = get_chart_8_9_data()
col1, col2 = st.columns(2)
with col1:
    chart_8_9_phase = st.selectbox('Phase du covid', get_covid_phases_labels_in_list(), index=2, key=3)

with col2:
    chart_8_9_compare = st.selectbox('Comparer avec', compare_with_year, index=1, key=4)

chart_8_9 = process_chart_8_9(chart_8_9_data, chart_8_9_phase, chart_8_9_compare)
st.plotly_chart(chart_8_9, use_container_width=True)


# CHART 10
st.header('Evolution de la part de production d\'énergie par filières (en %)')
chart_10_data = get_chart_7_data(datetime(2019, 1, 1).strftime('%Y-%m-%d'),datetime(2022, 12, 30).strftime('%Y-%m-%d'))
col1, col2 = st.columns(2)
with col1:
    chart_10_phase = st.selectbox('Phase du covid', get_covid_phases_labels_in_list(), index=2, key=5)

with col2:
    chart_10_compare = st.selectbox('Comparer avec', compare_with_year, index=1, key=6)

chart_10 = process_chart_10(chart_10_data, chart_10_phase, chart_10_compare)
st.plotly_chart(chart_10, use_container_width=True)
