import pandas as pd
import plotly.express as px
from contents.utils import covid_phases, energies, holidays_dates
from contents.sides import is_date_between
import plotly.graph_objects as go
from datetime import datetime

# Processing data manipulation to return chart 1 final dataframe
def get_chart_1_data(mask=True):
    df_cas_france = pd.read_csv('data/covid-cas-france.csv', delimiter=',') # Getting data from csv file might be replaced by API call
    chart_1_data = df_cas_france.loc[df_cas_france['pos'].notnull(), ['date', 'pos']] # Selecting non null necessary features
    chart_1_data['date'] = pd.to_datetime(chart_1_data['date'], format='%Y/%m/%d') # Converting date strings to date type
    chart_1_data['day'] = chart_1_data['date'].dt.day_name() # Adding a day name feature for each rows
   
    except_days = ['Saturday', 'Sunday', 'Monday'] 
    chart_1_data_no_we = chart_1_data.set_index('date') if mask else chart_1_data.loc[~chart_1_data['day'].isin(except_days)].set_index('date') # Excepting rows that are on mondays, saturdays and sundays if mask == False
    
    chart_mask = (~chart_1_data_no_we.index.strftime('%d%m').isin(holidays_dates)) # Formatting mask to keep only rows that are not corresponding to holiday dates   
    return chart_1_data_no_we.loc[chart_mask] # Final chart data

# Processing plotly manipulations to return chart 1 plot
def process_chart_1(chart_1_global_data):
    chart_1 = px.line(
        chart_1_global_data.reset_index(), 
        x="date", 
        y="pos", 
        labels={
                        "date": "Date",
                        "pos": "Nombre de cas",
        }
    )
    for covid_phase in covid_phases: # Adding vertical spans/lines for each covid phase
        if covid_phase['type'] == 'span':
            chart_1.add_vrect(x0=covid_phase['min'], x1=covid_phase['max'], line_width=0, fillcolor=covid_phase['color'], opacity=0.3, annotation_text=covid_phase['label'], annotation_textangle=90)
        else:
            chart_1.add_vline(x=covid_phase['min'], line_color=covid_phase['color'])
            chart_1.add_annotation(
                x=covid_phase['min'],
                text=covid_phase['label'],
                textangle=270,
            )
    return chart_1

def get_chart_7_data(start_date, end_date):
    df_ener_2019 = pd.read_csv('data/part-energies/xls/part-energies-2019.xls', sep='\t', encoding='latin-1', index_col=False, usecols=lambda x: x not in [' Stockage batterie', 'DÈstockage batterie', 'Eolien terrestre', 'Eolien offshore'])
    df_ener_2020 = pd.read_csv('data/part-energies/xls/part-energies-2020.xls', sep='\t', encoding='latin-1', index_col=False,usecols=lambda x: x not in [' Stockage batterie', 'DÈstockage batterie', 'Eolien terrestre', 'Eolien offshore'])
    df_ener_2021 = pd.read_csv('data/part-energies/xls/part-energies-2021-debut-2022.xls', sep='\t', encoding='latin-1', index_col=False,usecols=lambda x: x not in [' Stockage batterie', 'DÈstockage batterie', 'Eolien terrestre', 'Eolien offshore'])
    df_ener_2022 = pd.read_csv('data/part-energies/xls/part-energies-fin-2022.xls', sep='\t', encoding='latin-1', index_col=False,usecols=lambda x: x not in [' Stockage batterie', 'DÈstockage batterie', 'Eolien terrestre', 'Eolien offshore'])
    df_concat = pd.concat([df_ener_2019, df_ener_2020, df_ener_2021, df_ener_2022], ignore_index=True)
    df_concat = df_concat.loc[(~df_concat['Consommation'].isnull())]
    dates = pd.to_datetime(df_concat['Date'] + df_concat['Heures'], format='%Y-%m-%d%H:%M')
    df_concat.insert(1, "FullDate", dates)
    df_concat = df_concat.set_index('FullDate')
    return df_concat.loc[((df_concat['Date'] >= start_date) & (df_concat['Date'] <= end_date)), energies]

def process_chart_7(chart_7_data, start_date, end_date):
    data = []
    for energy in energies:
        data.append(go.Scatter(
            x = chart_7_data.index,
            y = chart_7_data[energy],
            stackgroup='one',
            name=energy
        ))
    chart_1 = go.Figure(
        data,
        layout=go.Layout(
            yaxis=dict(title="Production en MW"),
            xaxis=dict(title="Date")
        )
    )

    chart_1.update_layout(
        autosize=False,
        height=550,
    ) # Increasing chart height

    for covid_phase in covid_phases: # Adding vertical spans/lines for each covid phase
        range_min = datetime.strptime(start_date, "%Y-%m-%d") # Convert YYYY-MM-DD string into Python date object
        range_max = datetime.strptime(end_date, "%Y-%m-%d") # Convert YYYY-MM-DD string into Python date object
        if (is_date_between(datetime.strptime(covid_phase['min'], "%Y-%m-%d"), range_min, range_max) and (is_date_between(datetime.strptime(covid_phase['max'], "%Y-%m-%d"), range_min, range_max))): # If covid phase is in chart date range
            if covid_phase['type'] == 'span': # Add span type phase
                chart_1.add_vrect(x0=covid_phase['min'], x1=covid_phase['max'], line_width=0, fillcolor=covid_phase['color'], opacity=0.3, annotation_text=covid_phase['label'], annotation_textangle=90)
            else: # Add line type phase
                chart_1.add_vline(x=covid_phase['min'], line_color=covid_phase['color'])
                chart_1.add_annotation(
                    x=covid_phase['min'],
                    text=covid_phase['label'],
                    textangle=270,
                )
    return chart_1