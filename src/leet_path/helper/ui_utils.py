import pandas as pd
from dash import dash_table


def generate_table(df: pd.DataFrame):
    df = df.reset_index()
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_action='none',
        fixed_rows={'headers': True},
        style_table={'height': '400px', 'overflowY': 'auto'},
    )
