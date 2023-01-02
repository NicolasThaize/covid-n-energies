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
