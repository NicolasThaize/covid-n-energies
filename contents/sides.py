from datetime import datetime
from contents.utils import covid_phases

def chart_1_slide_start_date(dataframe):
    slide_start_date = get_df_oldest_date_index(dataframe)
    slide_start_date = convert_np_datetime64_to_date(slide_start_date)
    return datetime(slide_start_date.year, slide_start_date.month, slide_start_date.day) 

def chart_1_slide_end_date(dataframe):
    slide_start_date = get_df_youngest_date_index(dataframe)
    slide_start_date = convert_np_datetime64_to_date(slide_start_date)
    return datetime(slide_start_date.year, slide_start_date.month, slide_start_date.day)  

def get_df_oldest_date_index(df):
    return df.iloc[:1].index

def get_df_youngest_date_index(df):
    return df.iloc[-1:].index

def convert_np_datetime64_to_date(datetime):
    print(datetime)
    return datetime.item()

def is_date_between(date, min, max):
    return (min <= date <= max)

def get_rows_by_date_range(df, date_range):
    phase_1 = df.copy()
    phase_1 = phase_1.loc[((df['Date'] >= date_range['min']) & (df['Date'] <= date_range['max']))]
    return phase_1

def change_year_string(date_string, number_year_add):
    date_string_split = date_string.split('-')
    year_int = int(date_string_split[0]) + number_year_add
    date_string_split[0] = str(year_int)
    return "-".join(date_string_split)

def get_df_moved_year(df_global, move_year_by, base_df_date_range):
    phase_2_range = base_df_date_range.copy()
    phase_2_range['min'] = change_year_string(phase_2_range['min'] ,move_year_by)
    phase_2_range['max'] = change_year_string(phase_2_range['max'] ,move_year_by)

    phase_2 = df_global.copy()
    phase_2 = phase_2.loc[((df_global['Date'] >= phase_2_range['min']) & (df_global['Date'] <= phase_2_range['max']))]
    return phase_2

def process_evolution_percentage(df1,df2):
    sub = df2.reset_index().select_dtypes('number').subtract(df1.reset_index().select_dtypes('number'), axis=0)
    div = sub.divide(df1.reset_index().select_dtypes('number'), axis=0)
    return div.loc[~div['Fioul'].isnull()] *100

def generate_xticks_labels(df1, df2):
    date = df1.index.strftime('%m-%d %H:%M').tolist()
    date = [s + " - " for s in date]
    year_1 = df1.index.strftime('%Y').tolist()
    year_1 = [s + "/" for s in year_1]
    year_2 = df2.index.strftime('%Y').tolist()
    x_axis_labels = list(map(str.__add__, date, year_1))
    x_axis_labels = list(map(str.__add__, x_axis_labels, year_2))
    return x_axis_labels

def get_percentages(row):
    total = int(row.sum(axis=1).values[0])
    return row.applymap(lambda p: p/total*100)


def get_covid_phases_labels_in_list():
    return [covid_phase["label"] for covid_phase in covid_phases]

def sum_columns_values(df, columns, new_name):
    df_clean = df.copy()
    col = df.loc[:, columns].sum(axis=1)
    df_clean.drop(columns, axis=1, inplace=True)
    df_clean.insert(1, new_name, col)
    return df_clean