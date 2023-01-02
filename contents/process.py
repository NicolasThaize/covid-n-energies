import pandas as pd
from contents.utils import holidays_dates
import plotly.express as px
from contents.utils import covid_phases

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
        title='Nombre de nouveaux cas en France',
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
        title='Consommation brute d\'électricté en France (MW)',
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
        title='Consommation brute de gaz en France (MW)',
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
