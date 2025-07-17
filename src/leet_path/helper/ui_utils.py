import pandas as pd
from dash import dash_table
from dash.dash_table import FormatTemplate

from src.leet_path.helper import consts

WIDTHS = {
    consts.INDEX: '10%',
    consts.TITLE: '40%',
    consts.DIFFICULTY: '12.5%',
    consts.ACCEPTANCE: '12.5%',
}


def _append_tags(existing_tags, tag_cols, new_tags):
    existing_tags = existing_tags.copy()
    if tag_cols:
        tag_cols = [x for x in tag_cols if x in existing_tags]
        for col in tag_cols:
            old_tags = existing_tags.get(col, {})
            existing_tags[col] = {**old_tags, **new_tags}
    return existing_tags


def generate_table(df: pd.DataFrame, md_cols=None, pct_cols=None, dec_cols=None):
    df = df.reset_index()
    all_tags = {i: {'name': i, 'id': i} for i in df.columns}
    all_tags = _append_tags(all_tags, md_cols, {'presentation': 'markdown'})
    all_tags = _append_tags(all_tags, pct_cols, {'type': 'numeric', 'format': FormatTemplate.percentage(decimals=2)})
    all_tags = _append_tags(all_tags, dec_cols, {'type': 'numeric', 'format': {'specifier': '.3f'}})

    return dash_table.DataTable(
        data=df.to_dict(orient='records'),
        columns=list(all_tags.values()),
        style_cell={'textAlign': 'center', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
        style_cell_conditional=[{'if': {'column_id': k}, 'width': v} for k, v in WIDTHS.items()],
        markdown_options={'link_target': '_blank'},
        page_size=10,
        # page_action='none',
        # fixed_rows={'headers': True},
        # style_table={'height': '400px', 'overflowY': 'auto'},
    )
