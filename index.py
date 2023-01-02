import streamlit as st
import plotly.express as px
import  streamlit_toggle as tog

from contents.process import load_data, chart_1_global
from contents.sides import chart_1_slide_start_date, chart_1_slide_end_date
from contents.utils import covid_phases

st.title('Data Storytelling Covid19 - Énergies')

st.text(load_data())


# CHART 1
chart_1_toggle = tog.st_toggle_switch(
    label="Afficher les lundi, vendredi et samedi", 
    key="Key1", 
    default_value=False, 
    label_after = False, 
    inactive_color = '#D3D3D3', 
    active_color="#11567f", 
    track_color="#29B5E8"
)
chart_1_global_data = chart_1_global(chart_1_toggle) # Loading whole chart data
chart_1 = px.line(
    chart_1_global_data.reset_index(), 
    x="date", 
    y="pos", 
    title='Nombre de nouveaux cas en France',
    labels={
                     "date": "Date",
                     "pos": "Nombre de cas",
    }
)
for covid_phase in covid_phases:
    if covid_phase['type'] == 'span':
        chart_1.add_vrect(x0=covid_phase['min'], x1=covid_phase['max'], line_width=0, fillcolor=covid_phase['color'], opacity=0.3, annotation_text=covid_phase['label'], annotation_textangle=90)
    else:
        chart_1.add_vline(x=covid_phase['min'], line_color=covid_phase['color'])
        chart_1.add_annotation(
            x=covid_phase['min'],
            text=covid_phase['label'],
            textangle=270,
        )
st.plotly_chart(chart_1)