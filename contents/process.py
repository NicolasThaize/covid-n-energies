import pandas as pd
import datetime
from contents.utils import holidays_dates
import streamlit as st


@st.cache
def load_data():
    df_cas_france = pd.read_csv('data/covid-cas-france.csv', delimiter=',')
    return df_cas_france.shape

# Processing data manipulation to return chart 1 final dataframe
def chart_1_global(mask=True):
    df_cas_france = pd.read_csv('data/covid-cas-france.csv', delimiter=',') # Getting data from csv file might be replaced by API call
    chart_1_data = df_cas_france.loc[df_cas_france['pos'].notnull(), ['date', 'pos']] # Selecting non null necessary features
    chart_1_data['date'] = pd.to_datetime(chart_1_data['date'], format='%Y/%m/%d') # Converting date strings to date type
    chart_1_data['day'] = chart_1_data['date'].dt.day_name() # Adding a day name feature for each rows
   
    except_days = ['Saturday', 'Sunday', 'Monday'] 
    chart_1_data_no_we = chart_1_data.set_index('date') if mask else chart_1_data.loc[~chart_1_data['day'].isin(except_days)].set_index('date') # Excepting rows that are on mondays, saturdays and sundays
    
    chart_mask = (~chart_1_data_no_we.index.strftime('%d%m').isin(holidays_dates)) # Formatting mask to keep only rows that are not corresponding to holiday dates   
    return chart_1_data_no_we.loc[chart_mask] # Final chart data
