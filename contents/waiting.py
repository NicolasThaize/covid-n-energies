

import plotly.graph_objects as go

# Processing data manipulation to return chart 3 final dataframe
def chart_3_global():
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


# CHART 3
chart_3_global_data = chart_3_global() # Loading whole chart data
chart_3 = px.line(
    chart_3_global_data.reset_index(), 
    x=chart_3_global_data.index 
    y="pos", 
    title='Nombre de nouveaux cas en France',
    labels={
                     "date": "Date",
                     "pos": "Nombre de cas",
    }
)
for covid_phase in covid_phases:
    if covid_phase['type'] == 'span':
        chart_3.add_vrect(x0=covid_phase['min'], x1=covid_phase['max'], line_width=0, fillcolor=covid_phase['color'], opacity=0.3, annotation_text=covid_phase['label'], annotation_textangle=90)
    else:
        chart_3.add_vline(x=covid_phase['min'], line_color=covid_phase['color'])
        chart_3.add_annotation(
            x=covid_phase['min'],
            text=covid_phase['label'],
            textangle=270,
        )
st.plotly_chart(chart_3)

# fig = go.Figure()

# fig.add_trace(go.Scatter(
#     x=chart_3_global_data.index, 
#     y=chart_3_global_data["Conso_elec_totale_MW"],
#     mode='markers',
#     name='Mesures brutes',
#     marker_color=chart_3_global_data["Conso_elec_totale_MW"],
#     marker=dict(opacity=0.1,size=2)
# ))

# fig.add_trace(go.Scatter(
#     x=chart_3_global_data.index, 
#     y=chart_3_global_data["MA_max_7j"],
#     mode='lines',
#     name='Moy. Mobile Max hebdo'
# ))

# fig.update_layout(title='Consommation electrique en MW depuis 2018 en France')

# fig.show()
