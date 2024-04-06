# %%
import pandas as pd
import json, os
from constants import DATA_FOLDER

# %%

# %%
print("::Files found::")
print(os.listdir(DATA_FOLDER))

# %%
def load_data(folder):
    items = []
    json_files = [file for file in os.listdir(folder) if file.endswith(".json")]
    for file in json_files:
        item = json.load(open(os.path.join(folder, file), 'r'))
        items.extend(item)
    return items
businesses = load_data(DATA_FOLDER)
len(businesses)

# %%
import pandas as pd
import numpy as np

def calculate_percentiles(df, column_name):
    """
    Calculate the 10th, 25th, 50th (median), 75th, and 90th percentiles of a specified column in a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column_name (str): The name of the column to calculate the percentiles for.

    Returns:
    dict: A dictionary containing the percentiles.
    """
    percentiles = [10, 25, 50, 75, 90]
    percentile_values = np.percentile(df[column_name], percentiles)
    
    percentile_dict = {f"{p}th percentile": value for p, value in zip(percentiles, percentile_values)}
    
    return percentile_dict

def clean_str_to_int(number_string):
    if number_string:
      return int(number_string.replace("$", "").replace(",", ""))
    else:
      return None 
# Example usage (assuming you have a DataFrame `df` and a column of interest `column_name`)
# df = pd.DataFrame({'column_name': np.random.rand(100)})  # Example DataFrame
# print(calculate_percentiles(df, 'column_name'))

def save_csv_file(df, file_name="deals_"):
    from datetime import datetime
    today = datetime.now().isoformat().replace(":", ".")
    output_folder = os.path.join(DATA_FOLDER, 'csvs')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    df.to_csv(os.path.join(output_folder, file_name + today + ".csv"))


# %%
#businesses[0]

# %%
businesses_df = pd.DataFrame.from_records(businesses)
#businesses_df.head()

# %%
#businesses_df['cashflow'].unique()

businesses_df['asking_price_f'] = businesses_df['asking_price'].apply(clean_str_to_int )
businesses_df['cashflow_f'] = businesses_df['cashflow'].apply(clean_str_to_int)
businesses_df['P/E'] = businesses_df['asking_price_f']/businesses_df['cashflow_f']
percentiles = calculate_percentiles(businesses_df, 'P/E') 
print(percentiles)

save_csv_file(businesses_df)

# %%
import plotly.express as px

fig = px.histogram(businesses_df, x="P/E")
fig.save(os.path.join(DATA_FOLDER, 'pe_histogram.html'))

# %%
# %%
# %%



