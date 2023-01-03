from datetime import datetime

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