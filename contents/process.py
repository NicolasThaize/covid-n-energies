import pandas as pd
import plotly.express as px
from contents.utils import covid_phases, energies, holidays_dates
from contents.sides import is_date_between, get_rows_by_date_range, get_df_moved_year, process_evolution_percentage, generate_xticks_labels, get_percentages
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# Processing data manipulation to return chart 1 final dataframe
def get_chart_3_4_data():
    df_source = pd.read_csv("data/consommation-quotidienne-brute.csv", delimiter=";")

    df_energie = df_source.drop(columns=[
    "Date","Heure",
    "Consommation brute gaz (MW PCS 0°C) - GRTgaz",
    "Statut - GRTgaz","Consommation brute gaz (MW PCS 0°C) - Teréga",
    "Statut - Teréga"])

    df_energie.columns=["Date","Conso_gaz_totale_MW","Conso_elec_totale_MW","Statut","Conso_brute_totale_MW"]

    # Convertit la colonne date au format Str. 
    # utc n'est que True ou False
    df_energie["Date"] = pd.to_datetime(df_energie["Date"], utc=True)
    # On repasse donc en heure FR
    df_energie["Date"] = df_energie["Date"].dt.tz_convert('Europe/Paris')

    # Les données sont en ordre décroissant, les plus récentes en 1er.
    # On se replace en ordre chronologique
    df_energie.sort_values(by=["Date"], ascending=True, inplace=True)
    df_energie.reset_index(drop=True, inplace=True)

    # passage de la colonne date en index
    df_energie.set_index('Date', inplace=True)

    # Les mesures de ce Dataset sont arrêtées au 31/05/2022
    df_energie = df_energie.loc [ df_energie.index < "2022-06-01" ]

    df_energie = df_energie.loc [ df_energie.index < "2022-06-01" ]

    df_energie["Conso_gaz_totale_MW"] = df_energie["Conso_gaz_totale_MW"].interpolate(method='linear', axis=0)
    df_energie["Conso_brute_totale_MW"] = df_energie["Conso_brute_totale_MW"].interpolate(method='linear', axis=0)

    rolling_max_7j = df_energie["Conso_elec_totale_MW"].rolling(
        window=336,       # Moyenne mobile Hebdo (48x30mn x 7j)
        center=True,      
        min_periods=168,  # débute à la moitié de la fenêtre définie
    ).max()

    df_energie["MA_max_7j"] = rolling_max_7j

    df_last_3y = df_energie.loc[df_energie.index >= '2018-01-01']

    return df_last_3y # Final chart data

# Processing plotly manipulations to return chart 3 plot
def process_chart_3(chart_3_global_data):
    chart_3 = px.line(
        chart_3_global_data.reset_index(), 
        x=chart_3_global_data.index, 
        y=chart_3_global_data["Conso_elec_totale_MW"], 
        labels={
            "x": "Date",
            "y": "Consommation (MW)",
        }
    )
    for covid_phase in covid_phases: # Adding vertical spans/lines for each covid phase
        if covid_phase['type'] == 'span':
            chart_3.add_vrect(x0=covid_phase['min'], x1=covid_phase['max'], line_width=0, fillcolor=covid_phase['color'], opacity=0.3, annotation_text=covid_phase['label'], annotation_textangle=90)
        else:
            chart_3.add_vline(x=covid_phase['min'], line_color=covid_phase['color'])
            chart_3.add_annotation(
                x=covid_phase['min'],
                text=covid_phase['label'],
                textangle=270,
            )
    return chart_3

# Processing plotly manipulations to return chart 4 plot
def process_chart_4(chart_4_global_data):
    chart_4 = px.line(
        chart_4_global_data.reset_index(), 
        x=chart_4_global_data.index, 
        y=chart_4_global_data["Conso_gaz_totale_MW"], 
        labels={
            "x": "Date",
            "y": "Consommation (MW)",
        }
    )
    for covid_phase in covid_phases: # Adding vertical spans/lines for each covid phase
        if covid_phase['type'] == 'span':
            chart_4.add_vrect(x0=covid_phase['min'], x1=covid_phase['max'], line_width=0, fillcolor=covid_phase['color'], opacity=0.3, annotation_text=covid_phase['label'], annotation_textangle=90)
        else:
            chart_4.add_vline(x=covid_phase['min'], line_color=covid_phase['color'])
            chart_4.add_annotation(
                x=covid_phase['min'],
                text=covid_phase['label'],
                textangle=270,
            )
    return chart_4


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
    whole_energies = energies.copy()
    whole_energies.extend(['Date', 'Heures'])
    return df_concat.loc[((df_concat['Date'] >= start_date) & (df_concat['Date'] <= end_date)), whole_energies]

def process_chart_7(chart_7_data, start_date, end_date):
    data = []
    chart_7_data = chart_7_data.loc[:, energies]
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

def process_chart_10(chart_10_data):
    date_range = covid_phases[0]
    phase_1 = get_rows_by_date_range(chart_10_data, date_range)
    phase_2 = get_df_moved_year(chart_10_data, 1, date_range)

    phase_1_percentage = get_percentages(phase_1.loc[:, energies])
    phase_2_percentage = get_percentages(phase_2.loc[:, energies])
    evolution = process_evolution_percentage(phase_1_percentage, phase_2_percentage)
    x_axis_labels = generate_xticks_labels(phase_1_percentage, phase_2_percentage)
    final_data = evolution.loc[~evolution['Fioul'].isnull()]
    final_data.index = x_axis_labels

    fig = make_subplots(rows=2, cols=4)
    row = 1
    col = 1
    for energy in energies:
        fig.add_trace(
            go.Scatter(x=final_data.index, 
            y=final_data[energy],
            name=energy
            ),
            row=row, 
            col=col
        )
        col = col + 1
        if col == 5:
            col = 1
            row = 2
    
    fig.update_layout(height=1200)

    return fig

